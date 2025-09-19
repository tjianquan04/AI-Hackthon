import React, { useEffect, useState, useMemo } from 'react';

const parseCsv = (text) => {
  const rows = [];
  let i = 0, field = '', row = [], inQuotes = false;
  while (i < text.length) {
    const char = text[i];
    if (inQuotes) {
      if (char === '"') {
        if (text[i + 1] === '"') { field += '"'; i += 2; continue; }
        inQuotes = false; i++; continue;
      } else { field += char; i++; continue; }
    } else {
      if (char === '"') { inQuotes = true; i++; continue; }
      if (char === ',') { row.push(field); field = ''; i++; continue; }
      if (char === '\n' || char === '\r') {
        // handle CRLF or LF
        if (char === '\r' && text[i + 1] === '\n') i++;
        row.push(field); rows.push(row); row = []; field = ''; i++; continue;
      }
      field += char; i++;
    }
  }
  // flush last field
  if (field.length > 0 || row.length) { row.push(field); rows.push(row); }
  return rows;
};

const fetchPredictions = async () => {
  const tryFetch = async (url) => {
    const r = await fetch(url);
    if (!r.ok) throw new Error(`Failed to load ${url}`);
    return r.text();
  };
  let text = '';
  try { text = await tryFetch('/data/predictions_with_reasons.csv'); } catch (_) {}
  if (!text) {
    try { text = await tryFetch('http://localhost:8000/outputs/explanations/predictions_with_reasons.csv'); } catch (e) {
      console.error('Failed to fetch predictions CSV:', e);
      return [];
    }
  }
  const rows = parseCsv(text.trim());
  if (!rows.length) return [];
  const headers = rows[0];
  const records = rows.slice(1).filter(r => r.length && r.some(c => c && c.trim().length)).map((cols, idx) => {
    const obj = {};
    headers.forEach((h, i) => { obj[h] = cols[i]; });
    obj.id = idx + 1;
    // numeric fields
    const numericFields = ['Churn_Probability'];
    numericFields.forEach((f) => {
      const n = Number(obj[f]);
      obj[f] = Number.isFinite(n) ? n : null;
    });
    // label normalization
    obj.Predicted_Label = obj.Predicted_Label === '1' ? 'Churn' : 'No Churn';
    return obj;
  });
  return records;
};

const PredictView = () => {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const data = await fetchPredictions();
        if (mounted) setRows(data);
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => { mounted = false; };
  }, []);

  const filtered = useMemo(() => {
    const q = search.toLowerCase();
    return rows.filter(r =>
      String(r.Predicted_Label || '').toLowerCase().includes(q) ||
      String(r.Recommended_Action || '').toLowerCase().includes(q) ||
      String(r.Top_Reasons || '').toLowerCase().includes(q) ||
      String(r.Reason_Comment || '').toLowerCase().includes(q)
    );
  }, [rows, search]);

  if (loading) return (
    <div className="p-6 pt-20">
      <div className="text-gray-600">Loading predictions…</div>
    </div>
  );

  return (
    <div className="p-6 pt-20">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Predict New Churn</h1>
        <p className="text-gray-600">Model outputs with SHAP-based explanations</p>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-4">
        <input
          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
          placeholder="Search label, action, reason…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">#</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Probability</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Predicted</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Top Reasons</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SHAP Comment</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filtered.map((r) => (
                <tr key={r.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{r.id}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{r.Churn_Probability != null ? `${(r.Churn_Probability * 100).toFixed(1)}%` : '—'}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${r.Predicted_Label === 'Churn' ? 'text-red-600 bg-red-100' : 'text-green-600 bg-green-100'}`}>{r.Predicted_Label}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-pre-wrap text-sm text-gray-900">{r.Recommended_Action || '—'}</td>
                  <td className="px-6 py-4 whitespace-pre-wrap text-sm text-gray-700" style={{maxWidth:'420px'}}>{r.Top_Reasons || '—'}</td>
                  <td className="px-6 py-4 whitespace-pre-wrap text-sm text-gray-700" style={{maxWidth:'420px'}}>{r.Reason_Comment || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default PredictView;


