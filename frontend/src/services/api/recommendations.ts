import type { Recommendation } from "@/types/recommendation";
import { apiClient } from "./client";

export async function getCustomerRecommendations(
  customerId: string,
): Promise<Recommendation[]> {
  return apiClient<Recommendation[]>(
    `/api/v1/customers/${customerId}/recommendations`,
  );
}

export async function generateCustomerRecommendation(
  customerId: string,
): Promise<Recommendation> {
  return apiClient<Recommendation>(
    `/api/v1/customers/${customerId}/recommendations/generate`,
    {
      method: "POST",
    },
  );
}