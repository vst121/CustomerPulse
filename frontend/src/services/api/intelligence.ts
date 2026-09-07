import type { CustomerIntelligence } from "@/types/customerIntelligence";
import { apiClient } from "./client";

export async function getCustomerIntelligence(
  customerId: string,
): Promise<CustomerIntelligence> {
  return apiClient<CustomerIntelligence>(
    `/api/v1/customers/${customerId}/intelligence`,
  );
}