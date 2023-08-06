#pragma once

#include <ogdf/basic/Graph.h>
#include <ogdf/basic/simple_graph_alg.h>
#include <ogdf/basic/extended_graph_alg.h>
#include <ogdf/decomposition/StaticSPQRTree.h>
#include <ogdf/basic/LayoutModule.h>

#include <ogdf/planarlayout/FPPLayout.h>
#include <ogdf/basic/PreprocessorLayout.h>
#include <ogdf/packing/ComponentSplitterLayout.h>

#include <ogdf/layered/SugiyamaLayout.h>
#include <ogdf/layered/OptimalHierarchyLayout.h>

namespace ogdf_pythonization {

//std::unique_ptr<ogdf::LayoutModule> planar_layout;
//std::unique_ptr<ogdf::LayoutModule> non_planar_layout;

//void initLayoutModules() {
//    auto *pre = new ogdf::PreprocessorLayout();
//    planar_layout.reset(pre);
//    pre->setRandomizePositions(false);
//    auto *split = new ogdf::ComponentSplitterLayout();
//    pre->setLayoutModule(split);
//    split->setBorder(150);
//    auto *act = new ogdf::FPPLayout();
//    split->setLayoutModule(act);
//    act->separation(50);
//
//    auto *sugi = new ogdf::SugiyamaLayout();
//    non_planar_layout.reset(sugi);
//    sugi->minDistCC(150);
//    sugi->runs(1);
//    auto *ohl = new ogdf::OptimalHierarchyLayout();
//    sugi->setLayout(ohl);
//    ohl->nodeDistance(50);
//}

void spreadParallels(ogdf::GraphAttributes &GA, double min_spread = 0.1, double max_spread = 0.6, double max_abs = 100) {
    max_abs /= 2;
    GA.clearAllBends();
    ogdf::EdgeArray<ogdf::List<ogdf::edge>> parallels(GA.constGraph());
    ogdf::getParallelFreeUndirected(GA.constGraph(), parallels);
    for (auto e : GA.constGraph().edges) {
        if (parallels[e].empty()) continue;
        double spread = std::min(min_spread, max_spread / parallels[e].size());
        double width = spread * parallels[e].size();
        parallels[e].pushFront(e);

        ogdf::DPoint vec = GA.point(e->target()) - GA.point(e->source());
        ogdf::DPoint mid = GA.point(e->source()) + (vec / 2);
        ogdf::DPoint ort = vec.orthogonal();
        ort *= vec.norm() / ort.norm();
        if (ort.norm() > max_abs) {
            ort *= max_abs / ort.norm();
        }

        int idx = 0;
        for (auto pe:parallels[e]) {
            GA.bends(pe).pushBack(mid + ort * (-width / 2 + idx * spread));
            idx++;
        }
    }
}

void bendEdge(ogdf::GraphAttributes &GA, ogdf::edge e, double bend) {
    ogdf::DPoint vec = GA.point(e->target()) - GA.point(e->source());
    ogdf::DPoint mid = GA.point(e->source()) + (vec / 2);
    ogdf::DPoint ort = vec.orthogonal();
    ort *= vec.norm() / ort.norm();
    GA.bends(e).pushBack(mid + ort * bend);
}

//void renderSPQR(const ogdf::GraphAttributes &GA, const ogdf::StaticSPQRTree &spqr,
//                ogdf::Graph &C, ogdf::ClusterGraph &CG, ogdf::ClusterGraphAttributes &CA,
//                ogdf::LayoutModule* = nullptr) {
//    CA.init(ogdf::ClusterGraphAttributes::all ^ ogdf::GraphAttributes::edgeArrow);
//    CG.setUpdateDepth(true);
//    CA.directed() = false;
//    ogdf::EdgeArray<double> C_edge_length(C, 1);
//
//    ogdf::NodeArray<ogdf::node> node_C_to_skel(C);
//    ogdf::EdgeArray<ogdf::edge> edge_C_to_skel(C);
//    ogdf::ClusterArray<ogdf::node> cluster_to_spqr_node(CG);
//    ogdf::ClusterArray<ogdf::NodeArray<ogdf::node>> cluster_node_skel_to_C(CG);
//    ogdf::ClusterArray<ogdf::EdgeArray<ogdf::edge>> cluster_edge_skel_to_C(CG);
//    ogdf::NodeArray<ogdf::cluster> spqr_node_to_cluster(spqr.tree());
//
//    double cluster_spread = (GA.constGraph().numberOfNodes() * 50.0) / spqr.tree().numberOfNodes();
//    int spqr_node_nr = 0;
//    for (auto spqr_node : spqr.tree().nodes) {
//        ogdf::cluster cluster = CG.createEmptyCluster(CG.rootCluster());
//        cluster_to_spqr_node[cluster] = spqr_node;
//        spqr_node_to_cluster[spqr_node] = cluster;
//
//        std::stringstream ss;
//        switch (spqr.typeOf(spqr_node)) {
//            case ogdf::SPQRTree::NodeType::SNode:
//                ss << "S";
//                break;
//            case ogdf::SPQRTree::NodeType::PNode:
//                ss << "P";
//                break;
//            case ogdf::SPQRTree::NodeType::RNode:
//                ss << "R";
//                break;
//        }
//        ss << " (" << spqr_node_nr << ")";
//        CA.label(cluster) = ss.str();
//        CA.strokeType(cluster) = ogdf::StrokeType::Dash;
//
//        ogdf::Skeleton &skel = spqr.skeleton(spqr_node);
//        ogdf::Graph &skelg = skel.getGraph();
//        ogdf::NodeArray<ogdf::node> &node_skel_to_C = cluster_node_skel_to_C[cluster];
//        node_skel_to_C.init(skelg, nullptr);
//        ogdf::EdgeArray<ogdf::edge> &edge_skel_to_C = cluster_edge_skel_to_C[cluster];
//        edge_skel_to_C.init(skelg, nullptr);
//
//        for (auto vs: skelg.nodes) {
//            ogdf::node vc = C.newNode();
//            node_skel_to_C[vs] = vc;
//            node_C_to_skel[vc] = vs;
//            CG.reassignNode(vc, cluster);
//
//            CA.label(vc) = GA.label(skel.original(vs));
//            CA.shape(vc) = ogdf::Shape::Ellipse;
//            CA.x(vc) = cluster->index() * cluster_spread
//                       + vc->index() * 50 + (vc->index() % 3 - 1) * 5;
//            CA.y(vc) = cluster->index() * cluster_spread
//                       + vc->index() * 50 + (vc->index() % 3 - 1) * 5;
//        }
//
//        for (auto es: skelg.edges) {
//            ogdf::edge ec = C.newEdge(node_skel_to_C[es->source()], node_skel_to_C[es->target()]);
//            edge_skel_to_C[es] = ec;
//            edge_C_to_skel[ec] = es;
//        }
//
//        spqr_node_nr++;
//    }
//
//    ogdf::EdgeArray<ogdf::edge> twins(C, nullptr);
//    for (auto edge1 : C.edges) {
//        if (twins[edge1]) continue;
//
//        ogdf::cluster cluster1 = CG.clusterOf(edge1->source());
//        ogdf::node spqr_node1 = cluster_to_spqr_node[cluster1];
//        ogdf::node spqr_node2 = spqr.skeleton(spqr_node1).twinTreeNode(edge_C_to_skel[edge1]);
//        if (spqr_node2) { // virtual edge
//            ogdf::edge spqr_node2_skel_edge2 = spqr.skeleton(spqr_node1).twinEdge(edge_C_to_skel[edge1]);
//            ogdf::cluster cluster2 = spqr_node_to_cluster[spqr_node2];
//            ogdf::edge edge2 = cluster_edge_skel_to_C[cluster2][spqr_node2_skel_edge2];
//
//            twins[edge1] = edge2;
//            twins[edge2] = edge1;
//        } else { // we found a real edge
//            ogdf::edge real_edge = spqr.skeleton(spqr_node1).realEdge(edge_C_to_skel[edge1]);
//            CA.label(edge1) = GA.label(real_edge);
//            CA.strokeWidth(edge1) = 2.0f;
//            twins[edge1] = nullptr;
//        }
//    }
//
//    ogdf::EdgeArray<ogdf::edge> splits(C, nullptr);
//    for (auto edge1:C.edges) {
//        ogdf::edge edge2 = twins[edge1];
//        if (!edge2 || edge1->index() > edge2->index()) continue;
//        ogdf::edge edge1p = C.split(edge1);
//        splits[edge1] = edge1p;
//        ogdf::edge edge2p = C.split(edge2);
//        splits[edge2] = edge2p;
//        CG.reassignNode(edge1p->source(), CG.clusterOf(edge1p->target()));
//        CG.reassignNode(edge2p->source(), CG.clusterOf(edge2p->target()));
//        ogdf::edge new_edge = C.newEdge(edge1p->source(), edge2p->source());
//
//        CA.type(edge1p->source()) = ogdf::Graph::NodeType::dummy;
//        CA.width(edge1p->source()) = 1;
//        CA.height(edge1p->source()) = 1;
//        CA.type(edge2p->source()) = ogdf::Graph::NodeType::dummy;
//        CA.width(edge2p->source()) = 1;
//        CA.height(edge2p->source()) = 1;
//        CA.strokeColor(new_edge) = ogdf::Color(ogdf::Color::Name::Gray);
//
//        C_edge_length[edge1] = 0.5;
//        C_edge_length[edge1p] = 0.5;
//        C_edge_length[edge2] = 0.5;
//        C_edge_length[edge2p] = 0.5;
//        C_edge_length[new_edge] = 2;
//    }
//
//    fmmm.call(CA, C_edge_length);
//    CA.updateClusterPositions();
//    spreadParallels(CA);
//
//    for (auto edge1:C.edges) {
//        ogdf::edge edge2 = splits[edge1];
//        if (!edge2) continue;
//        OGDF_ASSERT(edge1->target() == edge2->source());
//        OGDF_ASSERT(CA.bends(edge1).empty());
//        OGDF_ASSERT(CA.bends(edge2).empty());
//        C.moveTarget(edge1, edge2->target());
//        CA.bends(edge1).pushBack(CA.point(edge2->source()));
//        C.delEdge(edge2);
//    }
//}

void setLabels(ogdf::GraphAttributes &GA, bool force = false) {
    for (auto n : GA.constGraph().nodes) {
        if (force || GA.label(n).empty()) {
            std::stringstream ss;
            ss << n->index();
            GA.label(n) = ss.str();
        }
    }

    for (auto e : GA.constGraph().edges) {
        if (force || GA.label(e).empty()) {
            std::stringstream ss;
            ss << e->index();
            GA.label(e) = ss.str();
        }
    }
}

}
