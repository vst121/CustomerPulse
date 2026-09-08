export type TransactionStatus =
  | "PENDING"
  | "COMPLETED"
  | "FAILED"
  | "REVERSED";

export type TransactionCategory =
  | "GROCERIES"
  | "RESTAURANT"
  | "TRAVEL"
  | "SHOPPING"
  | "UTILITIES"
  | "ENTERTAINMENT"
  | "OTHER";

export type Transaction = {
  id: string;
  customer_id: string;
  amount: string;
  currency: string;
  category: TransactionCategory;
  status: TransactionStatus;
  timestamp: string;
};

export type TransactionListResponse = {
  items: Transaction[];
  page: number;
  page_size: number;
  total: number;
};

export type CreateTransactionRequest = {
  amount: string;
  currency: string;
  category: TransactionCategory;
  status?: TransactionStatus;
  timestamp: string;
};