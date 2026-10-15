export type TaskStatus = 
  | 'pending'
  | 'planning'
  | 'awaiting_approval'
  | 'running'
  | 'paused'
  | 'completed'
  | 'failed'
  | 'cancelled';

export type TaskPriority = 'low' | 'medium' | 'high' | 'critical';
export type TaskMode = 'autonomous' | 'human_in_the_loop';

export interface SubTask {
  id: string;
  task_id: string;
  title: string;
  description?: string;
  assigned_agent: string;
  status: 'pending' | 'running' | 'awaiting_approval' | 'completed' | 'failed' | 'skipped';
  execution_order: number;
  dependencies: string[];
  tools_assigned: string[];
  input_data?: Record<string, any>;
  output_data?: Record<string, any>;
  error?: string;
  duration_ms: number;
  started_at?: string;
  completed_at?: string;
}

export interface Plan {
  id: string;
  task_id: string;
  total_steps: number;
  estimated_tokens: number;
  summary?: string;
  requires_approval: boolean;
  is_approved: boolean;
  created_at: string;
  subtasks: SubTask[];
}

export interface ApprovalRequest {
  id: string;
  task_id: string;
  subtask_id?: string;
  action_type: string;
  title: string;
  description: string;
  parameters: Record<string, any>;
  payload_hash: string;
  status: 'pending' | 'approved' | 'rejected' | 'modified';
  decision_notes?: string;
  decided_by?: string;
  requested_at: string;
  decided_at?: string;
}

export interface TaskDetail {
  id: string;
  title: string;
  objective: string;
  context?: string;
  status: TaskStatus;
  priority: TaskPriority;
  mode: TaskMode;
  progress_pct: number;
  validation_score?: number;
  final_deliverable?: string;
  error_message?: string;
  created_at: string;
  updated_at: string;
  completed_at?: string;
  subtasks: SubTask[];
  plan?: Plan;
  pending_approvals: ApprovalRequest[];
}

export interface TaskListResponse {
  tasks: TaskDetail[];
  total: number;
  active_count: number;
  completed_count: number;
  failed_count: number;
}

export interface AgentInfo {
  id: string;
  name: string;
  role: string;
  description: string;
  system_prompt: string;
  authorized_tools: string[];
  status: string;
  total_tasks_executed: number;
  successful_tasks: number;
  avg_duration_ms: number;
}

export interface ToolDefinition {
  name: string;
  description: string;
  category: string;
  is_sensitive: boolean;
  requires_approval: boolean;
  timeout_seconds: number;
  parameters: Array<{
    name: string;
    type: string;
    description: string;
    required: boolean;
    default?: any;
  }>;
  output_schema: Record<string, any>;
}

export interface SystemSettings {
  project_name: string;
  version: string;
  ai_provider: string;
  gemini_configured: boolean;
  openai_configured: boolean;
  anthropic_configured: boolean;
  max_subtasks: number;
  max_retries: number;
  task_timeout_seconds: number;
  auto_approve_safe_tools: boolean;
  available_providers: string[];
}

export interface SystemHealth {
  status: 'HEALTHY' | 'DEGRADED';
  service: string;
  version: string;
  database_connected: boolean;
  uptime_seconds: number;
  ai_provider: string;
  system_metrics: {
    ram_usage_pct: number;
    cpu_count: number;
  };
}

export interface ArtifactItem {
  id: string;
  task_id: string;
  file_name: string;
  file_type: string;
  size_bytes: number;
  content_summary?: string;
  created_at?: string;
}
