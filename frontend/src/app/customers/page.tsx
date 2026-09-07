export default function CustomersPage() {
  return (
    <main className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="px-8 py-6">
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Customers
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Manage customers and understand their lifecycle.
          </p>
        </div>
      </header>

      <section className="p-8">
        <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4">
            <div>
              <h2 className="font-semibold text-slate-900">Customer List</h2>

              <p className="mt-1 text-sm text-slate-500">
                Customers will be loaded from the CustomerPulse API.
              </p>
            </div>

            <button
              type="button"
              className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
            >
              Add Customer
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-slate-200 bg-slate-50">
                <tr>
                  <th className="px-6 py-3 font-medium text-slate-500">
                    Customer
                  </th>

                  <th className="px-6 py-3 font-medium text-slate-500">
                    Email
                  </th>

                  <th className="px-6 py-3 font-medium text-slate-500">
                    Lifecycle
                  </th>

                  <th className="px-6 py-3 font-medium text-slate-500">
                    Created
                  </th>

                  <th className="px-6 py-3 font-medium text-slate-500">
                    Action
                  </th>
                </tr>
              </thead>

              <tbody>
                <tr>
                  <td
                    colSpan={5}
                    className="px-6 py-12 text-center text-slate-500"
                  >
                    No customers loaded yet.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>
  );
}
