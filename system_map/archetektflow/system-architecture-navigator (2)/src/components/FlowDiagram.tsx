import React, { useMemo, useCallback } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  MiniMap,
  Node,
  Edge,
  MarkerType,
  ConnectionMode,
  Panel,
  Handle,
  Position,
  NodeProps
} from 'reactflow';
import 'reactflow/dist/style.css';
import { 
  Database, 
  Cpu, 
  Monitor, 
  Brain, 
  User, 
  Activity, 
  GitBranch, 
  ShieldCheck, 
  Zap, 
  FileText, 
  LayoutDashboard,
  BarChart3,
  Server,
  Cloud
} from 'lucide-react';

interface FlowDiagramProps {
  onNodeClick: (nodeId: string) => void;
  nodeStatuses: Record<string, "neutral" | "in-progress" | "complete">;
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'complete': return '#10b981'; // emerald-500
    case 'in-progress': return '#f59e0b'; // amber-500
    default: return '#64748b'; // slate-500
  }
};

const getStatusGlow = (status: string) => {
  switch (status) {
    case 'complete': return '0 0 15px rgba(16, 185, 129, 0.3)';
    case 'in-progress': return '0 0 15px rgba(245, 158, 11, 0.3)';
    default: return 'none';
  }
};

// --- CUSTOM NODE COMPONENTS ---

const getCategoryColor = (category?: string) => {
  switch (category) {
    case 'infra': return '#3b82f6'; // blue-500
    case 'data': return '#06b6d4'; // cyan-500
    case 'macro': return '#a855f7'; // purple-500
    case 'ai': return '#6366f1'; // indigo-500
    case 'risk': return '#f59e0b'; // amber-500
    case 'exec': return '#10b981'; // emerald-500
    case 'report': return '#94a3b8'; // slate-400
    case 'ui': return '#60a5fa'; // blue-400
    case 'aras': return '#ef4444'; // red-500
    case 'sched': return '#f97316'; // orange-500
    default: return '#64748b';
  }
};

const BaseNode = ({ data, selected, status, icon: Icon, shape = 'rounded' }: any) => {
  const statusColor = getStatusColor(status);
  const categoryColor = getCategoryColor(data.category);
  const glow = getStatusGlow(status);
  
  // Use category color if status is neutral, otherwise use status color
  const activeColor = status !== 'neutral' ? statusColor : categoryColor;

  const shapeStyles: Record<string, string> = {
    rounded: 'rounded-lg',
    cylinder: 'rounded-[20px/40px]',
    hexagon: 'clip-path-hexagon',
    circle: 'rounded-full',
    diamond: 'rotate-45',
  };

  return (
    <div 
      className={`group relative flex flex-col items-center justify-center p-3 transition-all duration-300 ${selected ? 'scale-105' : ''}`}
      style={{ 
        minWidth: '140px',
        minHeight: '60px',
      }}
    >
      <Handle type="target" position={Position.Top} className="!bg-slate-600 !w-2 !h-2" />
      
      <div 
        className={`relative flex flex-col items-center gap-2 border-2 p-3 backdrop-blur-sm transition-all duration-300 ${shapeStyles[shape] || 'rounded-lg'}`}
        style={{ 
          borderColor: activeColor,
          backgroundColor: status !== 'neutral' ? `${activeColor}33` : 'rgba(15, 23, 42, 0.9)',
          boxShadow: selected ? `0 0 20px ${activeColor}44` : glow,
          width: '100%',
          height: '100%',
        }}
      >
        {/* Shape-specific content rotation for diamond */}
        <div className={`${shape === 'diamond' ? '-rotate-45' : ''} flex flex-col items-center gap-1`}>
          {Icon && <Icon size={18} className="transition-colors" style={{ color: activeColor }} />}
          <div className="text-[11px] font-bold text-slate-100 text-center leading-tight">
            {data.label.split('\n').map((line: string, i: number) => (
              <div key={i}>{line}</div>
            ))}
          </div>
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} className="!bg-slate-600 !w-2 !h-2" />
    </div>
  );
};

const DatabaseNode = (props: NodeProps) => <BaseNode {...props} icon={Database} shape="cylinder" status={props.data.status} />;
const EngineNode = (props: NodeProps) => <BaseNode {...props} icon={Cpu} shape="rounded" status={props.data.status} />;
const UINode = (props: NodeProps) => <BaseNode {...props} icon={Monitor} shape="rounded" status={props.data.status} />;
const AINode = (props: NodeProps) => <BaseNode {...props} icon={Brain} shape="circle" status={props.data.status} />;
const HumanNode = (props: NodeProps) => <BaseNode {...props} icon={User} shape="rounded" status={props.data.status} />;
const FeedNode = (props: NodeProps) => <BaseNode {...props} icon={Activity} shape="rounded" status={props.data.status} />;
const GateNode = (props: NodeProps) => <BaseNode {...props} icon={GitBranch} shape="rounded" status={props.data.status} />;
const ShieldNode = (props: NodeProps) => <BaseNode {...props} icon={ShieldCheck} shape="rounded" status={props.data.status} />;
const ZapNode = (props: NodeProps) => <BaseNode {...props} icon={Zap} shape="rounded" status={props.data.status} />;
const LogNode = (props: NodeProps) => <BaseNode {...props} icon={FileText} shape="rounded" status={props.data.status} />;
const DashboardNode = (props: NodeProps) => <BaseNode {...props} icon={LayoutDashboard} shape="rounded" status={props.data.status} />;
const ChartNode = (props: NodeProps) => <BaseNode {...props} icon={BarChart3} shape="rounded" status={props.data.status} />;

const nodeTypes = {
  database: DatabaseNode,
  engine: EngineNode,
  ui: UINode,
  ai: AINode,
  human: HumanNode,
  feed: FeedNode,
  gate: GateNode,
  shield: ShieldNode,
  zap: ZapNode,
  log: LogNode,
  dashboard: DashboardNode,
  chart: ChartNode,
};

const FlowDiagram: React.FC<FlowDiagramProps> = ({ onNodeClick, nodeStatuses }) => {
  const nodes: Node[] = useMemo(() => [
    // --- INFRASTRUCTURE ---
    { id: 'Infra', data: { label: 'The Fortress: Cloud Infrastructure' }, position: { x: 0, y: 0 }, style: { width: 420, height: 220, backgroundColor: 'rgba(15, 23, 42, 0.4)', border: '1px dashed #334155', color: '#64748b', fontSize: 10, fontWeight: 'bold', borderRadius: 16 }, type: 'group' },
    { id: 'AWS_ECS', type: 'engine', data: { label: 'AWS Fargate/ECS\nCompute Engine', status: nodeStatuses['AWS_ECS'], category: 'infra' }, position: { x: 30, y: 50 }, parentId: 'Infra', extent: 'parent' },
    { id: 'AWS_RDS', type: 'database', data: { label: 'AWS RDS Postgres\nRelational DB', status: nodeStatuses['AWS_RDS'], category: 'infra' }, position: { x: 220, y: 50 }, parentId: 'Infra', extent: 'parent' },
    { id: 'AWS_Redis', type: 'database', data: { label: 'Redis ElastiCache\nReal-time State', status: nodeStatuses['AWS_Redis'], category: 'infra' }, position: { x: 125, y: 130 }, parentId: 'Infra', extent: 'parent' },

    // --- DATA FEEDS (L1) ---
    { id: 'Data_Feeds', data: { label: 'Level 1: External Data & Ingestion Senses' }, position: { x: 480, y: 0 }, style: { width: 700, height: 380, backgroundColor: 'rgba(15, 23, 42, 0.4)', border: '1px dashed #334155', color: '#64748b', fontSize: 10, fontWeight: 'bold', borderRadius: 16 }, type: 'group' },
    { id: 'DF_Price', type: 'feed', data: { label: 'Market Prices', status: nodeStatuses['DF_Price'], category: 'data' }, position: { x: 20, y: 50 }, parentId: 'Data_Feeds', extent: 'parent' },
    { id: 'DF_Macro', type: 'feed', data: { label: 'FRED Macro', status: nodeStatuses['DF_Macro'], category: 'data' }, position: { x: 170, y: 50 }, parentId: 'Data_Feeds', extent: 'parent' },
    { id: 'DF_PMI', type: 'feed', data: { label: 'S&P Global PMI', status: nodeStatuses['DF_PMI'], category: 'data' }, position: { x: 320, y: 50 }, parentId: 'Data_Feeds', extent: 'parent' },
    { id: 'DF_Crypto', type: 'feed', data: { label: 'Crypto Micro', status: nodeStatuses['DF_Crypto'], category: 'data' }, position: { x: 470, y: 50 }, parentId: 'Data_Feeds', extent: 'parent' },
    { id: 'DF_VIX', type: 'feed', data: { label: 'VIX & Options', status: nodeStatuses['DF_VIX'], category: 'data' }, position: { x: 20, y: 140 }, parentId: 'Data_Feeds', extent: 'parent' },
    { id: 'DF_SEC', type: 'feed', data: { label: 'SEC EDGAR', status: nodeStatuses['DF_SEC'], category: 'data' }, position: { x: 170, y: 140 }, parentId: 'Data_Feeds', extent: 'parent' },
    { id: 'DF_RSS', type: 'feed', data: { label: 'News RSS', status: nodeStatuses['DF_RSS'], category: 'data' }, position: { x: 320, y: 140 }, parentId: 'Data_Feeds', extent: 'parent' },
    { id: 'L1_Pipeline', type: 'gate', data: { label: 'L1 Ingestion\nData Aggregator', status: nodeStatuses['L1_Pipeline'], category: 'data' }, position: { x: 245, y: 260 }, parentId: 'Data_Feeds', extent: 'parent' },

    // --- SCHEDULING ---
    { id: 'Scheduling', data: { label: '⏰ Master Scheduler' }, position: { x: 1240, y: 0 }, style: { width: 260, height: 160, backgroundColor: 'rgba(249, 115, 22, 0.08)', border: '1px dashed #f97316', color: '#f97316', fontSize: 10, fontWeight: 'bold', borderRadius: 16 }, type: 'group' },
    { id: 'SCHED_Master', type: 'engine', data: { label: 'Master Scheduler\nAPScheduler', status: nodeStatuses['SCHED_Master'], category: 'sched' }, position: { x: 40, y: 55 }, parentId: 'Scheduling', extent: 'parent' },

    // --- MACRO COMPASS (L2) ---
    { id: 'L2', data: { label: 'Level 2: Macro Compass' }, position: { x: 0, y: 430 }, style: { width: 460, height: 180, backgroundColor: 'rgba(15, 23, 42, 0.4)', border: '1px dashed #334155', color: '#64748b', fontSize: 10, fontWeight: 'bold', borderRadius: 16 }, type: 'group' },
    { id: 'L2_Score', type: 'engine', data: { label: 'Regime Scoring', status: nodeStatuses['L2_Score'], category: 'macro' }, position: { x: 15, y: 60 }, parentId: 'L2', extent: 'parent' },
    { id: 'L2_RPE', type: 'engine', data: { label: 'Regime Probability', status: nodeStatuses['L2_RPE'], category: 'macro' }, position: { x: 160, y: 60 }, parentId: 'L2', extent: 'parent' },
    { id: 'L2_RSS', type: 'feed', data: { label: 'Retail Sentiment', status: nodeStatuses['L2_RSS'], category: 'macro' }, position: { x: 305, y: 60 }, parentId: 'L2', extent: 'parent' },

    // --- ARAS SUB-MODULES ---
    { id: 'ARAS_Modules', data: { label: 'ARAS Sub-Modules: Regime Inputs' }, position: { x: 480, y: 430 }, style: { width: 500, height: 310, backgroundColor: 'rgba(239, 68, 68, 0.05)', border: '1px dashed #ef4444', color: '#ef4444', fontSize: 10, fontWeight: 'bold', borderRadius: 16 }, type: 'group' },
    { id: 'ARAS_Delev', type: 'shield', data: { label: 'Deleveraging\nRisk', status: nodeStatuses['ARAS_Delev'], category: 'aras' }, position: { x: 20, y: 50 }, parentId: 'ARAS_Modules', extent: 'parent' },
    { id: 'ARAS_Margin', type: 'shield', data: { label: 'Margin\nStress', status: nodeStatuses['ARAS_Margin'], category: 'aras' }, position: { x: 180, y: 50 }, parentId: 'ARAS_Modules', extent: 'parent' },
    { id: 'ARAS_Gamma', type: 'shield', data: { label: 'Dealer\nGamma', status: nodeStatuses['ARAS_Gamma'], category: 'aras' }, position: { x: 340, y: 50 }, parentId: 'ARAS_Modules', extent: 'parent' },
    { id: 'ARAS_CryptoMicro', type: 'shield', data: { label: 'Crypto\nMicrostructure', status: nodeStatuses['ARAS_CryptoMicro'], category: 'aras' }, position: { x: 20, y: 140 }, parentId: 'ARAS_Modules', extent: 'parent' },
    { id: 'ARAS_PCR', type: 'shield', data: { label: 'Put/Call\nRegime', status: nodeStatuses['ARAS_PCR'], category: 'aras' }, position: { x: 180, y: 140 }, parentId: 'ARAS_Modules', extent: 'parent' },
    { id: 'ARAS_Shutdown', type: 'shield', data: { label: 'Shutdown\nRisk', status: nodeStatuses['ARAS_Shutdown'], category: 'aras' }, position: { x: 340, y: 140 }, parentId: 'ARAS_Modules', extent: 'parent' },
    { id: 'ARAS_Stress', type: 'shield', data: { label: 'Stress\nScenarios', status: nodeStatuses['ARAS_Stress'], category: 'aras' }, position: { x: 180, y: 230 }, parentId: 'ARAS_Modules', extent: 'parent' },

    // --- INTELLIGENCE (Expanded) ---
    { id: 'Intelligence', data: { label: 'Intelligence Layer: AI & Knowledge' }, position: { x: 1000, y: 430 }, style: { width: 500, height: 310, backgroundColor: 'rgba(99, 102, 241, 0.05)', border: '1px dashed #6366f1', color: '#6366f1', fontSize: 10, fontWeight: 'bold', borderRadius: 16 }, type: 'group' },
    { id: 'AI_Gateway', type: 'ai', data: { label: 'LLM Gateway\nGPT-5.4', status: nodeStatuses['AI_Gateway'], category: 'ai' }, position: { x: 20, y: 50 }, parentId: 'Intelligence', extent: 'parent' },
    { id: 'AI_ELVT', type: 'ai', data: { label: 'ELVT\nEarnings NLP', status: nodeStatuses['AI_ELVT'], category: 'ai' }, position: { x: 180, y: 50 }, parentId: 'Intelligence', extent: 'parent' },
    { id: 'AI_JPVI', type: 'ai', data: { label: 'JPVI\nJob Velocity', status: nodeStatuses['AI_JPVI'], category: 'ai' }, position: { x: 340, y: 50 }, parentId: 'Intelligence', extent: 'parent' },
    { id: 'AI_PFVT', type: 'ai', data: { label: 'PFVT\nPatent Filing', status: nodeStatuses['AI_PFVT'], category: 'ai' }, position: { x: 20, y: 140 }, parentId: 'Intelligence', extent: 'parent' },
    { id: 'AI_SCCR', type: 'ai', data: { label: 'SCCR\nSupply Chain', status: nodeStatuses['AI_SCCR'], category: 'ai' }, position: { x: 180, y: 140 }, parentId: 'Intelligence', extent: 'parent' },
    { id: 'AI_Gate3', type: 'ai', data: { label: 'Gate 3\nAnticipatory', status: nodeStatuses['AI_Gate3'], category: 'ai' }, position: { x: 340, y: 140 }, parentId: 'Intelligence', extent: 'parent' },
    { id: 'AI_KB', type: 'ai', data: { label: 'KB Ingest\nVector Store', status: nodeStatuses['AI_KB'], category: 'ai' }, position: { x: 180, y: 230 }, parentId: 'Intelligence', extent: 'parent' },

    // --- RISK & CONVICTION (L3) ---
    { id: 'L3', data: { label: 'Level 3: ARAS - Risk & Conviction' }, position: { x: 0, y: 790 }, style: { width: 1500, height: 440, backgroundColor: 'rgba(15, 23, 42, 0.2)', border: '1px dashed #334155', color: '#64748b', fontSize: 10, fontWeight: 'bold', borderRadius: 24 }, type: 'group' },
    
    { id: 'Thesis_Integrity', data: { label: 'Thesis Integrity' }, position: { x: 15, y: 50 }, parentId: 'L3', style: { width: 230, height: 350, backgroundColor: 'rgba(15, 23, 42, 0.4)', border: '1px solid #1e293b', borderRadius: 16 }, type: 'group' },
    { id: 'L3_SENTINEL', type: 'shield', data: { label: 'SENTINEL', status: nodeStatuses['L3_SENTINEL'], category: 'risk' }, position: { x: 15, y: 50 }, parentId: 'Thesis_Integrity', extent: 'parent' },
    { id: 'L3_TDC', type: 'shield', data: { label: 'TDC: Thesis Audit', status: nodeStatuses['L3_TDC'], category: 'risk' }, position: { x: 15, y: 140 }, parentId: 'Thesis_Integrity', extent: 'parent' },
    { id: 'L3_CDM', type: 'shield', data: { label: 'CDM: Supply Chain', status: nodeStatuses['L3_CDM'], category: 'risk' }, position: { x: 15, y: 230 }, parentId: 'Thesis_Integrity', extent: 'parent' },

    { id: 'Conviction_Sizing', data: { label: 'Sizing & Lifespan' }, position: { x: 260, y: 50 }, parentId: 'L3', style: { width: 230, height: 350, backgroundColor: 'rgba(15, 23, 42, 0.4)', border: '1px solid #1e293b', borderRadius: 16 }, type: 'group' },
    { id: 'L3_MICS', type: 'zap', data: { label: 'MICS: Conviction', status: nodeStatuses['L3_MICS'], category: 'risk' }, position: { x: 15, y: 50 }, parentId: 'Conviction_Sizing', extent: 'parent' },
    { id: 'L3_CDF', type: 'zap', data: { label: 'CDF: Decay', status: nodeStatuses['L3_CDF'], category: 'risk' }, position: { x: 15, y: 140 }, parentId: 'Conviction_Sizing', extent: 'parent' },
    { id: 'L3_CCM', type: 'zap', data: { label: 'CCM: Calibration', status: nodeStatuses['L3_CCM'], category: 'risk' }, position: { x: 15, y: 230 }, parentId: 'Conviction_Sizing', extent: 'parent' },

    { id: 'Defense_Hedges', data: { label: 'Defense & Safety' }, position: { x: 505, y: 50 }, parentId: 'L3', style: { width: 230, height: 350, backgroundColor: 'rgba(15, 23, 42, 0.4)', border: '1px solid #1e293b', borderRadius: 16 }, type: 'group' },
    { id: 'L3_PTRH', type: 'shield', data: { label: 'PTRH: Tail Hedge', status: nodeStatuses['L3_PTRH'], category: 'risk' }, position: { x: 15, y: 50 }, parentId: 'Defense_Hedges', extent: 'parent' },
    { id: 'L3_CAM', type: 'shield', data: { label: 'CAM: Coverage', status: nodeStatuses['L3_CAM'], category: 'risk' }, position: { x: 15, y: 140 }, parentId: 'Defense_Hedges', extent: 'parent' },
    { id: 'L3_DSHP', type: 'shield', data: { label: 'DSHP: Harvest', status: nodeStatuses['L3_DSHP'], category: 'risk' }, position: { x: 15, y: 230 }, parentId: 'Defense_Hedges', extent: 'parent' },

    { id: 'Offense_ReEntry', data: { label: 'Offense & Growth' }, position: { x: 750, y: 50 }, parentId: 'L3', style: { width: 230, height: 350, backgroundColor: 'rgba(15, 23, 42, 0.4)', border: '1px solid #1e293b', borderRadius: 16 }, type: 'group' },
    { id: 'L3_ARES', type: 'zap', data: { label: 'ARES: Re-Entry', status: nodeStatuses['L3_ARES'], category: 'risk' }, position: { x: 15, y: 50 }, parentId: 'Offense_ReEntry', extent: 'parent' },
    { id: 'L3_AUP', type: 'zap', data: { label: 'AUP: Asymmetric', status: nodeStatuses['L3_AUP'], category: 'risk' }, position: { x: 15, y: 140 }, parentId: 'Offense_ReEntry', extent: 'parent' },
    { id: 'L3_TRP', type: 'zap', data: { label: 'TRP: Retirement', status: nodeStatuses['L3_TRP'], category: 'risk' }, position: { x: 15, y: 230 }, parentId: 'Offense_ReEntry', extent: 'parent' },
    { id: 'L3_Safety', type: 'shield', data: { label: 'Incapacitation', status: nodeStatuses['L3_Safety'], category: 'risk' }, position: { x: 15, y: 310 }, parentId: 'Offense_ReEntry', extent: 'parent' },

    { id: 'Portfolio_Guards', data: { label: 'Portfolio Guards' }, position: { x: 995, y: 50 }, parentId: 'L3', style: { width: 490, height: 350, backgroundColor: 'rgba(15, 23, 42, 0.4)', border: '1px solid #1e293b', borderRadius: 16 }, type: 'group' },
    { id: 'L3_PDS', type: 'shield', data: { label: 'PDS: Drawdown\nSentinel', status: nodeStatuses['L3_PDS'], category: 'risk' }, position: { x: 20, y: 50 }, parentId: 'Portfolio_Guards', extent: 'parent' },
    { id: 'L3_FEM', type: 'shield', data: { label: 'FEM: Factor\nExposure', status: nodeStatuses['L3_FEM'], category: 'risk' }, position: { x: 20, y: 140 }, parentId: 'Portfolio_Guards', extent: 'parent' },
    { id: 'L3_Kevlar', type: 'shield', data: { label: 'Kevlar:\nConcentration', status: nodeStatuses['L3_Kevlar'], category: 'risk' }, position: { x: 20, y: 230 }, parentId: 'Portfolio_Guards', extent: 'parent' },
    { id: 'L3_SLOF', type: 'zap', data: { label: 'SLOF: Leverage\nOverlay', status: nodeStatuses['L3_SLOF'], category: 'risk' }, position: { x: 210, y: 50 }, parentId: 'Portfolio_Guards', extent: 'parent' },
    { id: 'L3_PERM', type: 'zap', data: { label: 'PERM: Premium\nExtraction', status: nodeStatuses['L3_PERM'], category: 'risk' }, position: { x: 210, y: 140 }, parentId: 'Portfolio_Guards', extent: 'parent' },

    // --- EXECUTION PIPELINE (L4-L6) ---
    { id: 'Execution_Pipeline', data: { label: 'Levels 4-6: Portfolio & Execution Pipeline' }, position: { x: 0, y: 1290 }, style: { width: 1500, height: 380, backgroundColor: 'rgba(15, 23, 42, 0.2)', border: '1px dashed #334155', color: '#64748b', fontSize: 10, fontWeight: 'bold', borderRadius: 24 }, type: 'group' },
    { id: 'L4_Master', type: 'engine', data: { label: 'L4: Master\nEngine', status: nodeStatuses['L4_Master'], category: 'exec' }, position: { x: 30, y: 60 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'EX_TOG', type: 'engine', data: { label: 'Trade Order\nGenerator', status: nodeStatuses['EX_TOG'], category: 'exec' }, position: { x: 200, y: 60 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'L5_Orders', type: 'engine', data: { label: 'L5: Order\nBook', status: nodeStatuses['L5_Orders'], category: 'exec' }, position: { x: 370, y: 60 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'EX_PAIE', type: 'shield', data: { label: 'PAIE: Pre-Exec\nIntegrity', status: nodeStatuses['EX_PAIE'], category: 'exec' }, position: { x: 540, y: 60 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'EX_LAEP', type: 'zap', data: { label: 'LAEP: VIX\nExecution', status: nodeStatuses['EX_LAEP'], category: 'exec' }, position: { x: 710, y: 60 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'EX_CB', type: 'shield', data: { label: 'Circuit\nBreaker', status: nodeStatuses['EX_CB'], category: 'exec' }, position: { x: 880, y: 60 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'L6_Queue', type: 'gate', data: { label: 'Confirmation\nQueue', status: nodeStatuses['L6_Queue'], category: 'exec' }, position: { x: 1050, y: 60 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'EX_Overnight', type: 'shield', data: { label: 'Overnight\nMonitor', status: nodeStatuses['EX_Overnight'], category: 'exec' }, position: { x: 30, y: 200 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'EX_Corr', type: 'engine', data: { label: 'Correlation\nMonitor', status: nodeStatuses['EX_Corr'], category: 'exec' }, position: { x: 200, y: 200 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'EX_Escal', type: 'shield', data: { label: 'Escalation\nEngine', status: nodeStatuses['EX_Escal'], category: 'exec' }, position: { x: 370, y: 200 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'EX_PMProtocol', type: 'human', data: { label: 'PM Co-Sign\nProtocol', status: nodeStatuses['EX_PMProtocol'], category: 'exec' }, position: { x: 540, y: 200 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'EX_StratQ', type: 'gate', data: { label: 'Strategic\nQueue', status: nodeStatuses['EX_StratQ'], category: 'exec' }, position: { x: 710, y: 200 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'EX_QueueGov', type: 'engine', data: { label: 'Queue\nGovernance', status: nodeStatuses['EX_QueueGov'], category: 'exec' }, position: { x: 880, y: 200 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'L6_Broker', type: 'engine', data: { label: 'L6: Execution\nAPI', status: nodeStatuses['L6_Broker'], category: 'exec' }, position: { x: 1050, y: 200 }, parentId: 'Execution_Pipeline', extent: 'parent' },
    { id: 'Exchange', type: 'database', data: { label: 'Market\nBrokers', status: nodeStatuses['Exchange'], category: 'exec' }, position: { x: 1250, y: 130 }, parentId: 'Execution_Pipeline', extent: 'parent' },

    // --- REPORTING (L7) ---
    { id: 'L7', data: { label: 'Level 7: Audit, Monitor & Analytics' }, position: { x: 0, y: 1730 }, style: { width: 1500, height: 200, backgroundColor: 'rgba(15, 23, 42, 0.2)', border: '1px dashed #334155', color: '#64748b', fontSize: 10, fontWeight: 'bold', borderRadius: 24 }, type: 'group' },
    { id: 'L7_Log', type: 'log', data: { label: 'Session Log', status: nodeStatuses['L7_Log'], category: 'report' }, position: { x: 30, y: 60 }, parentId: 'L7', extent: 'parent' },
    { id: 'L7_Daily', type: 'dashboard', data: { label: 'Daily Monitor', status: nodeStatuses['L7_Daily'], category: 'report' }, position: { x: 210, y: 60 }, parentId: 'L7', extent: 'parent' },
    { id: 'L7_PID', type: 'ai', data: { label: 'PID: Intel\nDigest', status: nodeStatuses['L7_PID'], category: 'report' }, position: { x: 390, y: 60 }, parentId: 'L7', extent: 'parent' },
    { id: 'L7_Analytics', type: 'chart', data: { label: 'Monthly\nAnalytics', status: nodeStatuses['L7_Analytics'], category: 'report' }, position: { x: 570, y: 60 }, parentId: 'L7', extent: 'parent' },
    { id: 'L7_EOD', type: 'log', data: { label: 'EOD\nSnapshot', status: nodeStatuses['L7_EOD'], category: 'report' }, position: { x: 750, y: 60 }, parentId: 'L7', extent: 'parent' },
    { id: 'L7_PerfAttr', type: 'chart', data: { label: 'Performance\nAttribution', status: nodeStatuses['L7_PerfAttr'], category: 'report' }, position: { x: 930, y: 60 }, parentId: 'L7', extent: 'parent' },
    { id: 'L7_RegimeHist', type: 'chart', data: { label: 'Regime\nHistory', status: nodeStatuses['L7_RegimeHist'], category: 'report' }, position: { x: 1110, y: 60 }, parentId: 'L7', extent: 'parent' },

    // --- DESKTOP UI ---
    { id: 'Desktop_UI', data: { label: '🖥️ The Cockpit: Desktop User Interface' }, position: { x: 0, y: 1990 }, style: { width: 1500, height: 260, backgroundColor: 'rgba(30, 58, 138, 0.15)', border: '1px solid #1e40af', color: '#60a5fa', fontSize: 12, fontWeight: 'bold', borderRadius: 24 }, type: 'group' },
    { id: 'UI_Dashboard', type: 'ui', data: { label: 'Main Dashboard', status: nodeStatuses['UI_Dashboard'], category: 'ui' }, position: { x: 50, y: 80 }, parentId: 'Desktop_UI', extent: 'parent' },
    { id: 'UI_ActionCenter', type: 'ui', data: { label: 'Action Center', status: nodeStatuses['UI_ActionCenter'], category: 'ui' }, position: { x: 350, y: 80 }, parentId: 'Desktop_UI', extent: 'parent' },
    { id: 'UI_ReportsTab', type: 'ui', data: { label: 'Reports & Logs', status: nodeStatuses['UI_ReportsTab'], category: 'ui' }, position: { x: 650, y: 80 }, parentId: 'Desktop_UI', extent: 'parent' },
    { id: 'Human_PM', type: 'human', data: { label: 'Human PM / GP', status: nodeStatuses['Human_PM'], category: 'ui' }, position: { x: 1000, y: 80 }, parentId: 'Desktop_UI', extent: 'parent' },
  ], [nodeStatuses]);

  const edges: Edge[] = useMemo(() => [
    // Infrastructure Connections
    { id: 'e-ecs-l4', source: 'AWS_ECS', target: 'L4_Master', style: { stroke: '#334155', strokeDasharray: '2,2' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    { id: 'e-rds-l7', source: 'AWS_RDS', target: 'L7_Log', style: { stroke: '#334155', strokeDasharray: '2,2' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    { id: 'e-redis-l5', source: 'AWS_Redis', target: 'L5_Orders', style: { stroke: '#334155', strokeDasharray: '2,2' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },

    // L1 Data Feed Connections
    { id: 'e-price-l1', source: 'DF_Price', target: 'L1_Pipeline', animated: true, style: { stroke: '#06b6d4' } },
    { id: 'e-macro-l1', source: 'DF_Macro', target: 'L1_Pipeline', animated: true, style: { stroke: '#06b6d4' } },
    { id: 'e-pmi-l1', source: 'DF_PMI', target: 'L1_Pipeline', animated: true, style: { stroke: '#06b6d4' } },
    { id: 'e-crypto-l1', source: 'DF_Crypto', target: 'L1_Pipeline', animated: true, style: { stroke: '#06b6d4' } },
    { id: 'e-vix-l1', source: 'DF_VIX', target: 'L1_Pipeline', animated: true, style: { stroke: '#06b6d4' } },
    { id: 'e-sec-l1', source: 'DF_SEC', target: 'L1_Pipeline', animated: true, style: { stroke: '#06b6d4' } },
    { id: 'e-rss-l1', source: 'DF_RSS', target: 'L1_Pipeline', animated: true, style: { stroke: '#06b6d4' } },
    
    // L1 to L2 Macro Compass
    { id: 'e-l1-l2', source: 'L1_Pipeline', target: 'L2_Score', label: 'Cleaned Data', labelStyle: { fill: '#94a3b8', fontSize: 10 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    { id: 'e-l1-l2-2', source: 'L1_Pipeline', target: 'L2_RPE', markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    
    // L1 to ARAS Sub-Modules
    { id: 'e-l1-aras', source: 'L1_Pipeline', target: 'ARAS_Delev', label: 'Market Data', labelStyle: { fill: '#94a3b8', fontSize: 10 }, style: { stroke: '#ef4444', strokeDasharray: '3,3' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#ef4444' } },
    { id: 'e-l1-aras2', source: 'L1_Pipeline', target: 'ARAS_Margin', style: { stroke: '#ef4444', strokeDasharray: '3,3' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#ef4444' } },
    { id: 'e-l1-aras3', source: 'L1_Pipeline', target: 'ARAS_Gamma', style: { stroke: '#ef4444', strokeDasharray: '3,3' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#ef4444' } },

    // ARAS to L3 Risk
    { id: 'e-aras-sentinel', source: 'ARAS_Stress', target: 'L3_SENTINEL', label: 'Regime Ceiling', labelStyle: { fill: '#94a3b8', fontSize: 10 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#ef4444' }, style: { stroke: '#ef4444' } },
    
    // L2 to L3
    { id: 'e-l2-l3', source: 'L2_Score', target: 'L3_SENTINEL', label: 'Regime Signal', labelStyle: { fill: '#94a3b8', fontSize: 10 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    { id: 'e-l2-l3-2', source: 'L2_RPE', target: 'L3_MICS', markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    
    // Intelligence Connections
    { id: 'e-l1-ai', source: 'L1_Pipeline', target: 'AI_Gateway', label: 'Context', labelStyle: { fill: '#94a3b8', fontSize: 10 }, style: { strokeDasharray: '5,5', stroke: '#6366f1' } },
    { id: 'e-ai-tdc', source: 'AI_Gateway', target: 'L3_TDC', label: 'Analysis', labelStyle: { fill: '#94a3b8', fontSize: 10 }, style: { strokeDasharray: '5,5', stroke: '#6366f1' } },
    { id: 'e-ai-elvt', source: 'AI_Gateway', target: 'AI_ELVT', style: { stroke: '#6366f1', strokeDasharray: '3,3' } },
    { id: 'e-ai-jpvi', source: 'AI_Gateway', target: 'AI_JPVI', style: { stroke: '#6366f1', strokeDasharray: '3,3' } },
    { id: 'e-elvt-sent', source: 'AI_ELVT', target: 'L3_SENTINEL', style: { stroke: '#6366f1', strokeDasharray: '5,5' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#6366f1' } },
    { id: 'e-gate3-sent', source: 'AI_Gate3', target: 'L3_SENTINEL', style: { stroke: '#6366f1', strokeDasharray: '5,5' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#6366f1' } },
    { id: 'e-sccr-cdm', source: 'AI_SCCR', target: 'L3_CDM', style: { stroke: '#6366f1', strokeDasharray: '5,5' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#6366f1' } },
    { id: 'e-kb-ai', source: 'AI_KB', target: 'AI_Gateway', label: 'KB Context', labelStyle: { fill: '#94a3b8', fontSize: 10 }, style: { stroke: '#6366f1' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#6366f1' } },
    
    // Scheduler Connections
    { id: 'e-sched-l4', source: 'SCHED_Master', target: 'L4_Master', style: { stroke: '#f97316', strokeDasharray: '4,4' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f97316' } },
    { id: 'e-sched-kb', source: 'SCHED_Master', target: 'AI_KB', style: { stroke: '#f97316', strokeDasharray: '4,4' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f97316' } },

    // L3 Internal Flow
    { id: 'e-l3-1', source: 'L3_SENTINEL', target: 'L3_MICS', markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    { id: 'e-l3-2', source: 'L3_MICS', target: 'L4_Master', label: 'Conviction', labelStyle: { fill: '#94a3b8', fontSize: 10 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#10b981' } },
    { id: 'e-pds-l4', source: 'L3_PDS', target: 'L4_Master', style: { stroke: '#f59e0b' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f59e0b' } },
    { id: 'e-fem-l4', source: 'L3_FEM', target: 'L4_Master', style: { stroke: '#f59e0b' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f59e0b' } },
    { id: 'e-kevlar-l4', source: 'L3_Kevlar', target: 'L4_Master', style: { stroke: '#f59e0b' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f59e0b' } },
    { id: 'e-slof-l5', source: 'L3_SLOF', target: 'L5_Orders', style: { stroke: '#f59e0b' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f59e0b' } },
    { id: 'e-perm-l5', source: 'L3_PERM', target: 'L5_Orders', style: { stroke: '#f59e0b' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f59e0b' } },
    
    // Execution Pipeline Flow
    { id: 'e-l4-tog', source: 'L4_Master', target: 'EX_TOG', animated: true, style: { stroke: '#10b981' } },
    { id: 'e-tog-l5', source: 'EX_TOG', target: 'L5_Orders', animated: true, style: { stroke: '#10b981' } },
    { id: 'e-l5-paie', source: 'L5_Orders', target: 'EX_PAIE', markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    { id: 'e-paie-laep', source: 'EX_PAIE', target: 'EX_LAEP', animated: true, style: { stroke: '#10b981' } },
    { id: 'e-laep-q', source: 'EX_LAEP', target: 'L6_Queue', markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    { id: 'e-cb-l5', source: 'EX_CB', target: 'L5_Orders', label: 'HALT', labelStyle: { fill: '#ef4444', fontSize: 10 }, style: { stroke: '#ef4444', strokeDasharray: '3,3' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#ef4444' } },
    { id: 'e-overnight-l4', source: 'EX_Overnight', target: 'L4_Master', style: { stroke: '#f59e0b', strokeDasharray: '3,3' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f59e0b' } },
    { id: 'e-corr-kevlar', source: 'EX_Corr', target: 'L3_Kevlar', style: { stroke: '#f59e0b', strokeDasharray: '3,3' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f59e0b' } },
    { id: 'e-escal-q', source: 'EX_Escal', target: 'L6_Queue', label: 'Block', labelStyle: { fill: '#ef4444', fontSize: 10 }, style: { stroke: '#ef4444', strokeDasharray: '3,3' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#ef4444' } },
    { id: 'e-pm-q', source: 'EX_PMProtocol', target: 'L6_Queue', label: 'Approve', labelStyle: { fill: '#10b981', fontSize: 10 }, style: { stroke: '#10b981' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#10b981' } },
    { id: 'e-q-stratq', source: 'L6_Queue', target: 'EX_StratQ', markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    { id: 'e-stratq-broker', source: 'EX_StratQ', target: 'L6_Broker', animated: true, style: { stroke: '#10b981' } },
    { id: 'e-qgov-q', source: 'EX_QueueGov', target: 'L6_Queue', style: { stroke: '#334155' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    { id: 'e-broker-exch', source: 'L6_Broker', target: 'Exchange', label: 'FIX/REST', labelStyle: { fill: '#94a3b8', fontSize: 10 }, animated: true, style: { stroke: '#10b981' } },
    
    // Reporting & UI Connections
    { id: 'e-l4-log', source: 'L4_Master', target: 'L7_Log', style: { stroke: '#334155' } },
    { id: 'e-eod-daily', source: 'L7_EOD', target: 'L7_Daily', style: { stroke: '#94a3b8' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#94a3b8' } },
    { id: 'e-perf-analytics', source: 'L7_PerfAttr', target: 'L7_Analytics', style: { stroke: '#94a3b8' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#94a3b8' } },
    { id: 'e-regime-l2', source: 'L7_RegimeHist', target: 'L2_Score', style: { stroke: '#94a3b8', strokeDasharray: '5,5' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#94a3b8' } },
    { id: 'e-log-reports', source: 'L7_Log', target: 'UI_ReportsTab', markerEnd: { type: MarkerType.ArrowClosed, color: '#334155' } },
    { id: 'e-daily-dash', source: 'L7_Daily', target: 'UI_Dashboard', animated: true, style: { stroke: '#60a5fa' } },
    { id: 'e-q-action', source: 'L6_Queue', target: 'UI_ActionCenter', label: 'Pending', labelStyle: { fill: '#f59e0b', fontSize: 10 }, animated: true, style: { stroke: '#f59e0b' } },
    { id: 'e-human-action', source: 'Human_PM', target: 'UI_ActionCenter', markerEnd: { type: MarkerType.ArrowClosed, color: '#60a5fa' } },
    { id: 'e-pm-human', source: 'EX_PMProtocol', target: 'Human_PM', style: { stroke: '#60a5fa', strokeDasharray: '5,5' }, markerEnd: { type: MarkerType.ArrowClosed, color: '#60a5fa' } },
  ], []);

  const onNodeClickInternal = useCallback((event: React.MouseEvent, node: Node) => {
    // Only trigger for leaf nodes (not groups)
    const groups = [
      'Infra', 'Data_Feeds', 'Scheduling', 'L2', 'ARAS_Modules', 'Intelligence', 'L3', 
      'Thesis_Integrity', 'Conviction_Sizing', 'Defense_Hedges', 
      'Offense_ReEntry', 'Portfolio_Guards', 'Execution_Pipeline', 'L7', 'Desktop_UI'
    ];
    
    if (!groups.includes(node.id)) {
      onNodeClick(node.id);
    }
  }, [onNodeClick]);

  return (
    <div style={{ width: '100%', height: '1000px', backgroundColor: '#020617', borderRadius: '12px', border: '1px solid #1e293b', overflow: 'hidden' }}>
      <style>
        {`
          .clip-path-hexagon {
            clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
          }
          .react-flow__node {
            cursor: pointer;
          }
          .react-flow__edge-path {
            stroke-width: 2;
            transition: stroke 0.3s;
          }
          .react-flow__edge:hover .react-flow__edge-path {
            stroke: #3b82f6 !important;
          }
        `}
      </style>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodeClick={onNodeClickInternal}
        nodeTypes={nodeTypes}
        connectionMode={ConnectionMode.Loose}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        style={{ backgroundColor: '#020617' }}
      >
        <Background color="#1e293b" gap={20} />
        <Controls />
        <MiniMap 
          nodeColor={(n) => {
            if (n.type === 'group') return '#1e293b';
            return getStatusColor(nodeStatuses[n.id] || 'neutral');
          }}
          maskColor="rgba(2, 6, 23, 0.7)"
          style={{ backgroundColor: '#0f172a', border: '1px solid #1e293b' }}
        />
        <Panel position="top-left" style={{ color: '#94a3b8', fontSize: '10px', fontWeight: 'bold' }}>
          ACHELION ARMS FLOW ENGINE v2.0
        </Panel>
      </ReactFlow>
    </div>
  );
};

export default FlowDiagram;
