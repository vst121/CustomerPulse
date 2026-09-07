export type LifecycleStage =
  | "ACQUISITION"
  | "ONBOARDING"
  | "ACTIVATION"
  | "ENGAGEMENT"
  | "GROWTH"
  | "RETENTION"
  | "WIN_BACK";

export type Customer = {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  lifecycle_stage: LifecycleStage;
  created_at: string;
};

export type CustomerListResponse = {
  items: Customer[];
  page: number;
  page_size: number;
  total: number;
};