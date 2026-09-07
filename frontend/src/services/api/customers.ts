import { apiClient } from "./client";
import type {
  Customer,
  CustomerListResponse,
  LifecycleStage,
} from "@/types/customer";
import type { Customer360 } from "@/types/customer360";

export type GetCustomersParams = {
  page?: number;
  page_size?: number;
  search?: string;
  lifecycle_stage?: LifecycleStage;
};

export async function getCustomers(
  params: GetCustomersParams = {},
): Promise<CustomerListResponse> {
  const searchParams = new URLSearchParams();

  if (params.page !== undefined) {
    searchParams.set("page", String(params.page));
  }

  if (params.page_size !== undefined) {
    searchParams.set("page_size", String(params.page_size));
  }

  if (params.search) {
    searchParams.set("search", params.search);
  }

  if (params.lifecycle_stage) {
    searchParams.set("lifecycle_stage", params.lifecycle_stage);
  }

  const query = searchParams.toString();

  return apiClient<CustomerListResponse>(
    `/api/v1/customers${query ? `?${query}` : ""}`,
  );
}

export async function getCustomer(
  customerId: string,
): Promise<Customer> {
  return apiClient<Customer>(
    `/api/v1/customers/${customerId}`,
  );
}

export async function getCustomer360(
  customerId: string,
): Promise<Customer360> {
  return apiClient<Customer360>(
    `/api/v1/customers/${customerId}/360`,
  );
}
