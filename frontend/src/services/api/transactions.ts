import type {
  CreateTransactionRequest,
  Transaction,
  TransactionListResponse,
} from "@/types/transaction";
import { apiClient } from "./client";

export type GetCustomerTransactionsParams = {
  page?: number;
  page_size?: number;
};

export async function getCustomerTransactions(
  customerId: string,
  params: GetCustomerTransactionsParams = {},
): Promise<TransactionListResponse> {
  const searchParams = new URLSearchParams();

  if (params.page !== undefined) {
    searchParams.set("page", String(params.page));
  }

  if (params.page_size !== undefined) {
    searchParams.set("page_size", String(params.page_size));
  }

  const query = searchParams.toString();

  return apiClient<TransactionListResponse>(
    `/api/v1/transactions/customers/${customerId}${
      query ? `?${query}` : ""
    }`,
  );
}

export async function getTransaction(
  transactionId: string,
): Promise<Transaction> {
  return apiClient<Transaction>(
    `/api/v1/transactions/${transactionId}`,
  );
}

export async function createTransaction(
  customerId: string,
  idempotencyKey: string,
  request: CreateTransactionRequest,
): Promise<Transaction> {
  return apiClient<Transaction>(
    `/api/v1/transactions/customers/${customerId}`,
    {
      method: "POST",
      headers: {
        "Idempotency-Key": idempotencyKey,
      },
      body: JSON.stringify(request),
    },
  );
}