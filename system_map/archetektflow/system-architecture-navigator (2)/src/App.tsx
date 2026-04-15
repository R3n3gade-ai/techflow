/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from "react";
import { 
  Sheet, 
  SheetContent, 
  SheetHeader, 
  SheetTitle, 
  SheetDescription,
  SheetFooter
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  CheckCircle2, 
  Clock, 
  Circle, 
  Info, 
  Layers, 
  Database, 
  Activity, 
  ShieldCheck,
  Zap,
  BarChart3,
  Link2,
  Settings,
  MessageSquare,
  Save
} from "lucide-react";
import FlowDiagram from "@/src/components/FlowDiagram";
import { nodeData, NodeInfo } from "@/src/nodeData";
import { motion, AnimatePresence } from "motion/react";

type NodeStatus = "neutral" | "in-progress" | "complete";

export default function App() {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  useEffect(() => {
    if (selectedNodeId) {
      console.log("App: Node selected:", selectedNodeId);
    }
  }, [selectedNodeId]);

  const [nodeStatuses, setNodeStatuses] = useState<Record<string, NodeStatus>>(() => {
    const initial: Record<string, NodeStatus> = {};
    Object.keys(nodeData).forEach(id => {
      initial[id] = "neutral";
    });
    return initial;
  });
  const [nodeNotes, setNodeNotes] = useState<Record<string, string>>(() => {
    const initial: Record<string, string> = {};
    Object.keys(nodeData).forEach(id => {
      initial[id] = "";
    });
    return initial;
  });

  const selectedNode = selectedNodeId ? nodeData[selectedNodeId] : null;

  const handleStatusChange = (status: NodeStatus) => {
    if (selectedNodeId) {
      setNodeStatuses(prev => ({
        ...prev,
        [selectedNodeId]: status
      }));
    }
  };

  const handleNoteChange = (note: string) => {
    if (selectedNodeId) {
      setNodeNotes(prev => ({
        ...prev,
        [selectedNodeId]: note
      }));
    }
  };

  const getStatusIcon = (status: NodeStatus) => {
    switch (status) {
      case "complete": return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
      case "in-progress": return <Clock className="w-4 h-4 text-amber-400" />;
      default: return <Circle className="w-4 h-4 text-slate-500" />;
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case "Infrastructure": return <Database className="w-4 h-4" />;
      case "Data Feeds": return <Activity className="w-4 h-4" />;
      case "Macro Compass": return <Layers className="w-4 h-4" />;
      case "Intelligence": return <Zap className="w-4 h-4" />;
      case "Risk & Conviction": return <ShieldCheck className="w-4 h-4" />;
      case "ARAS Sub-Modules": return <ShieldCheck className="w-4 h-4" />;
      case "Execution": return <Settings className="w-4 h-4" />;
      case "Reporting": return <BarChart3 className="w-4 h-4" />;
      case "Scheduling": return <Clock className="w-4 h-4" />;
      default: return <Info className="w-4 h-4" />;
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 font-sans selection:bg-slate-800 dark">
      {/* Header */}
      <header className="border-b border-slate-800 bg-[#020617]/80 backdrop-blur-md sticky top-0 z-10 px-6 py-4 flex items-center justify-between shadow-2xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center text-slate-900 shadow-lg">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white">Achelion ARMS Navigator</h1>
            <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">System Architecture & Status</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <Button 
            variant="ghost" 
            size="sm" 
            className="text-slate-400 hover:text-white hover:bg-slate-800"
            onClick={() => {
              const reset: Record<string, NodeStatus> = {};
              Object.keys(nodeData).forEach(id => {
                reset[id] = "neutral";
              });
              setNodeStatuses(reset);
            }}
          >
            Reset All
          </Button>
          <div className="flex items-center gap-6 px-4 py-2 bg-slate-900/50 rounded-full border border-slate-800">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-slate-800 border border-slate-600" />
              <span className="text-xs font-semibold text-slate-400">Neutral</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-amber-900/50 border border-amber-500" />
              <span className="text-xs font-semibold text-amber-400">In Progress</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-emerald-900/50 border border-emerald-500" />
              <span className="text-xs font-semibold text-emerald-400">Complete</span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6 lg:p-10">
        <div className="grid grid-cols-1 gap-8">
          {/* Main Diagram Area */}
          <section className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold flex items-center gap-2 text-white">
                <Activity className="w-5 h-5 text-slate-400" />
                Interactive Infrastructure Map
              </h2>
              <div className="flex items-center gap-2 text-sm text-slate-500 italic">
                <Info className="w-4 h-4" />
                Click any node to explore details and manage progress
              </div>
            </div>
            
            <FlowDiagram 
              onNodeClick={setSelectedNodeId}
              nodeStatuses={nodeStatuses}
            />
          </section>

          {/* Stats Summary */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card className="bg-slate-900/50 border-slate-800 shadow-xl">
              <CardHeader className="pb-2">
                <CardTitle className="text-xs font-bold text-slate-500 uppercase tracking-widest">Total Components</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-white">{Object.keys(nodeData).length}</div>
              </CardContent>
            </Card>
            <Card className="bg-slate-900/50 border-slate-800 shadow-xl">
              <CardHeader className="pb-2">
                <CardTitle className="text-xs font-bold text-slate-500 uppercase tracking-widest">In Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-amber-500">
                  {Object.values(nodeStatuses).filter(s => s === "in-progress").length}
                </div>
              </CardContent>
            </Card>
            <Card className="bg-slate-900/50 border-slate-800 shadow-xl">
              <CardHeader className="pb-2">
                <CardTitle className="text-xs font-bold text-slate-500 uppercase tracking-widest">Completed</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-emerald-500">
                  {Object.values(nodeStatuses).filter(s => s === "complete").length}
                </div>
              </CardContent>
            </Card>
            <Card className="bg-slate-900/50 border-slate-800 shadow-xl">
              <CardHeader className="pb-2">
                <CardTitle className="text-xs font-bold text-slate-500 uppercase tracking-widest">System Health</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-blue-400">
                  {Math.round((Object.values(nodeStatuses).filter(s => s === "complete").length / Object.keys(nodeData).length) * 100)}%
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      {/* Node Details Drawer */}
      <Sheet open={!!selectedNodeId} onOpenChange={(open) => !open && setSelectedNodeId(null)}>
        <SheetContent className="sm:max-w-xl bg-[#0f172a] border-l border-slate-800 shadow-2xl p-0 overflow-hidden flex flex-col">
          <AnimatePresence mode="wait">
            {selectedNode && (
              <motion.div
                key={selectedNode.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="h-full flex flex-col"
              >
                <div className="p-8 space-y-6 border-b border-slate-800 bg-[#020617]/50">
                  <div className="flex items-center justify-between">
                    <Badge variant="outline" className="flex items-center gap-1.5 px-3 py-1 bg-slate-900 text-slate-300 border-slate-700">
                      {getCategoryIcon(selectedNode.category)}
                      {selectedNode.category}
                    </Badge>
                    <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800">
                      {getStatusIcon(nodeStatuses[selectedNode.id])}
                      <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
                        {nodeStatuses[selectedNode.id].replace("-", " ")}
                      </span>
                    </div>
                  </div>
                  <SheetHeader className="space-y-2">
                    <SheetTitle className="text-3xl font-bold tracking-tight text-white leading-tight">
                      {selectedNode.title}
                    </SheetTitle>
                    <SheetDescription className="text-slate-500 text-xs font-mono bg-slate-900/50 p-2 rounded border border-slate-800 inline-block w-fit">
                      SYSTEM_NODE_ID: {selectedNode.id}
                    </SheetDescription>
                  </SheetHeader>
                </div>

                <ScrollArea className="flex-1 px-8 py-8">
                  <div className="space-y-10">
                    {/* Detailed Breakdown */}
                    <div className="space-y-8">
                      <div className="space-y-3">
                        <h3 className="text-xs font-bold uppercase tracking-[0.2em] text-blue-400 flex items-center gap-2">
                          <Zap className="w-4 h-4" />
                          What it does
                        </h3>
                        <p className="text-slate-300 leading-relaxed text-lg font-medium">
                          {selectedNode.whatItDoes || selectedNode.description}
                        </p>
                      </div>

                      {selectedNode.connectedTo && (
                        <div className="space-y-3">
                          <h3 className="text-xs font-bold uppercase tracking-[0.2em] text-purple-400 flex items-center gap-2">
                            <Link2 className="w-4 h-4" />
                            Connected to
                          </h3>
                          <p className="text-slate-400 leading-relaxed">
                            {selectedNode.connectedTo}
                          </p>
                        </div>
                      )}

                      {selectedNode.howItWorks && (
                        <div className="space-y-3">
                          <h3 className="text-xs font-bold uppercase tracking-[0.2em] text-emerald-400 flex items-center gap-2">
                            <Settings className="w-4 h-4" />
                            How it works
                          </h3>
                          <p className="text-slate-400 leading-relaxed bg-slate-900/30 p-4 rounded-lg border border-slate-800/50">
                            {selectedNode.howItWorks}
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Status Controls */}
                    <div className="space-y-4 pt-4 border-t border-slate-800">
                      <h3 className="text-xs font-bold uppercase tracking-[0.2em] text-slate-500 flex items-center gap-2">
                        <Activity className="w-4 h-4" />
                        Update Implementation Status
                      </h3>
                      <div className="grid grid-cols-3 gap-3">
                        <Button 
                          variant={nodeStatuses[selectedNode.id] === "neutral" ? "default" : "outline"}
                          className={`flex-col items-center justify-center gap-2 h-20 transition-all border-slate-800 ${nodeStatuses[selectedNode.id] === "neutral" ? "bg-slate-100 text-slate-900 hover:bg-white" : "text-slate-400 hover:bg-slate-800 hover:text-white"}`}
                          onClick={() => handleStatusChange("neutral")}
                        >
                          <Circle className="w-5 h-5" />
                          <span className="text-[10px] font-bold uppercase tracking-widest">Neutral</span>
                        </Button>
                        
                        <Button 
                          variant={nodeStatuses[selectedNode.id] === "in-progress" ? "default" : "outline"}
                          className={`flex-col items-center justify-center gap-2 h-20 transition-all border-slate-800 ${nodeStatuses[selectedNode.id] === "in-progress" ? "bg-amber-600 text-white hover:bg-amber-700" : "text-slate-400 hover:bg-slate-800 hover:text-white"}`}
                          onClick={() => handleStatusChange("in-progress")}
                        >
                          <Clock className="w-5 h-5" />
                          <span className="text-[10px] font-bold uppercase tracking-widest">In Progress</span>
                        </Button>
                        
                        <Button 
                          variant={nodeStatuses[selectedNode.id] === "complete" ? "default" : "outline"}
                          className={`flex-col items-center justify-center gap-2 h-20 transition-all border-slate-800 ${nodeStatuses[selectedNode.id] === "complete" ? "bg-emerald-600 text-white hover:bg-emerald-700" : "text-slate-400 hover:bg-slate-800 hover:text-white"}`}
                          onClick={() => handleStatusChange("complete")}
                        >
                          <CheckCircle2 className="w-5 h-5" />
                          <span className="text-[10px] font-bold uppercase tracking-widest">Complete</span>
                        </Button>
                      </div>
                    </div>

                    {/* Manual Notes */}
                    <div className="space-y-4 pt-4 border-t border-slate-800 pb-10">
                      <h3 className="text-xs font-bold uppercase tracking-[0.2em] text-slate-500 flex items-center gap-2">
                        <MessageSquare className="w-4 h-4" />
                        Manual Implementation Notes
                      </h3>
                      <div className="relative">
                        <textarea 
                          className="w-full h-40 bg-slate-900 border border-slate-800 rounded-xl p-4 text-slate-300 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all placeholder:text-slate-700"
                          placeholder="Add technical notes, blockers, or next steps for this component..."
                          value={nodeNotes[selectedNode.id]}
                          onChange={(e) => handleNoteChange(e.target.value)}
                        />
                        <div className="absolute bottom-3 right-3">
                          <Save className="w-4 h-4 text-slate-700" />
                        </div>
                      </div>
                    </div>
                  </div>
                </ScrollArea>

                <div className="p-6 border-t border-slate-800 bg-[#020617]/50">
                  <Button 
                    className="w-full h-12 bg-white text-slate-900 hover:bg-slate-200 font-bold uppercase tracking-widest text-xs"
                    onClick={() => setSelectedNodeId(null)}
                  >
                    Close Navigator
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </SheetContent>
      </Sheet>

      {/* Footer */}
      <footer className="p-10 text-center border-t border-slate-900 bg-[#020617]">
        <div className="max-w-4xl mx-auto space-y-4">
          <div className="flex items-center justify-center gap-2 text-slate-500 text-[10px] font-bold uppercase tracking-[0.3em]">
            <ShieldCheck className="w-4 h-4" />
            Achelion ARMS &bull; Self-Driving Portfolio Philosophy
          </div>
          <p className="text-slate-600 text-xs leading-relaxed max-w-2xl mx-auto italic">
            "Level 1 provides the cameras and sensors. Level 2 and the AI read the road signs and weather. Level 3 is the collision-avoidance system. Levels 4 through 6 are the steering wheel and pedals. Level 7 is the dashboard showing speed and mileage."
          </p>
        </div>
      </footer>
    </div>
  );
}
