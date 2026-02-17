import React, { useState } from 'react';
import { useKeycloak } from '@react-keycloak/web';

type ReportItem = {
  user_id: string;
  report_date: string;
  full_name: string | null;
  email: string | null;
  city: string | null;
  events_count: number;
  avg_battery_level: number;
  avg_signal_strength: number;
  loaded_at: string;
};

type ReportsResponse = {
  items: ReportItem[];
};

const ReportPage: React.FC = () => {
  const { keycloak, initialized } = useKeycloak();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [reports, setReports] = useState<ReportItem[]>([]);
  const [reportDate, setReportDate] = useState('');

  const downloadReport = async () => {
    if (!keycloak?.token) {
      setError('Not authenticated');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await keycloak.updateToken(30);

      const params = new URLSearchParams();
      if (reportDate) {
        params.set('date', reportDate);
      }
      const queryString = params.toString();

      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/reports${queryString ? `?${queryString}` : ''}`,
        {
        headers: {
          'Authorization': `Bearer ${keycloak.token}`
        }
      });

      if (response.status === 401) {
        setError('Session expired. Please login again.');
        keycloak.login();
        return;
      }

      if (response.status === 403) {
        setError('Access denied: you can load only your own reports.');
        return;
      }

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API error ${response.status}: ${errorText}`);
      }

      const data = await response.json() as ReportsResponse;
      setReports(data.items ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (!initialized) {
    return <div>Loading...</div>;
  }

  if (!keycloak.authenticated) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <button
          onClick={() => keycloak.login()}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Login
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6">Usage Reports</h1>

        <div className="mb-4">
          <label className="block text-sm mb-2" htmlFor="report-date">
            Date (optional)
          </label>
          <input
            id="report-date"
            type="date"
            value={reportDate}
            onChange={(e) => setReportDate(e.target.value)}
            className="px-3 py-2 border rounded w-full"
          />
        </div>

        <button
          onClick={downloadReport}
          disabled={loading}
          className={`px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 ${
            loading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {loading ? 'Generating Report...' : 'Download Report'}
        </button>

        {error && (
          <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        {!error && !loading && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">Results</h2>
            {reports.length === 0 ? (
              <p className="text-gray-600">No report rows found for selected period.</p>
            ) : (
              <div className="space-y-2">
                {reports.map((item, index) => (
                  <div key={`${item.user_id}-${item.report_date}-${index}`} className="p-3 border rounded">
                    <div><strong>User:</strong> {item.user_id}</div>
                    <div><strong>Date:</strong> {item.report_date}</div>
                    <div><strong>Events:</strong> {item.events_count}</div>
                    <div><strong>Battery avg:</strong> {item.avg_battery_level.toFixed(2)}</div>
                    <div><strong>Signal avg:</strong> {item.avg_signal_strength.toFixed(2)}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ReportPage;