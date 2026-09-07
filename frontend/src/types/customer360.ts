export type Customer360Transaction = {
  id: string;
  amount: string;
  currency: string;
  category: string;
  status: string;
  timestamp: string;
};

export type Customer360Recommendation = {
  id: string;
  type: string;
  reason: string;
};

export type Customer360 = {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  lifecycle_stage: string;
  created_at: string;
  value: {
    total_spend: string;
    transaction_count: number;
  };
  score: {
    score: string;
  };
  transactions: Customer360Transaction[];
  recommendations: Customer360Recommendation[];
};