export type CustomerIntelligence = {
  features: {
    transaction_count: number;
    total_transaction_value: string;
    average_transaction_value: string;
    days_since_last_transaction: number;
  };

  prediction: {
    churn_probability: string;
  };

  action: {
    action_type: string;
    priority: number;
    reason: string;
  };
};