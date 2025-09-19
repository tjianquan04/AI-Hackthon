// Load real data from /data (served by CRA via junction to D:\\AI Hackathon\\data)
export const generateCustomerData = async () => {
  const tryFetch = async (url) => {
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`Failed to load ${url}`);
    const text = await resp.text();
    return text;
  };

  // 1) Try CRA public /data
  let text;
  try {
    text = await tryFetch('/data/bank_churn_cleaned.csv');
  } catch (_) {
    text = '';
  }

  // If first non-space char is '<', it's likely HTML fallback; try python server
  const looksHtml = (s) => /<html|<!DOCTYPE/i.test(s.slice(0, 200));
  if (!text || looksHtml(text)) {
    try {
      text = await tryFetch('http://localhost:8000/data/bank_churn_cleaned.csv');
    } catch (e) {
      console.error('CSV fetch failed from /data and localhost:8000:', e);
      return [];
    }
  }

  const lines = text.trim().split(/\r?\n/);
  if (!lines.length) return [];
  const headers = lines[0].split(',');
  const hasClientNum = headers.includes('CLIENTNUM');

  const records = [];
  for (let i = 1; i < lines.length; i++) {
    const row = lines[i];
    if (!row) continue;
    const cols = row.split(',');
    const obj = {};
    headers.forEach((h, idx) => { obj[h] = cols[idx]; });
    // Synthesize CLIENTNUM if column is missing
    if (!hasClientNum) {
      obj.CLIENTNUM = 100000 + i; // stable per-file pseudo ID
    }
    // Basic numeric casting without producing NaN
    const numericFields = [
      'CLIENTNUM','Customer_Age','Dependent_count','Months_on_book','Total_Relationship_Count',
      'Months_Inactive_12_mon','Contacts_Count_12_mon','Credit_Limit','Total_Revolving_Bal',
      'Avg_Open_To_Buy','Total_Trans_Amt','Total_Trans_Ct','Avg_Utilization_Ratio'
    ];
    numericFields.forEach(f => {
      const v = obj[f];
      if (v === undefined || v === '') { obj[f] = null; return; }
      const n = Number(v);
      obj[f] = Number.isFinite(n) ? n : null;
    });
    records.push(obj);
  }
  return records;
};

// Calculate churn risk based on customer attributes
export const calculateChurnRisk = (customer) => {
  let riskScore = 0;
  if (customer.Customer_Age > 60) riskScore += 10; else if (customer.Customer_Age < 30) riskScore += 15;
  if (customer.Months_Inactive_12_mon > 3) riskScore += 20;
  if (customer.Contacts_Count_12_mon > 4) riskScore += 15;
  if (customer.Avg_Utilization_Ratio > 0.7) riskScore += 25; else if (customer.Avg_Utilization_Ratio < 0.1) riskScore += 10;
  if (customer.Total_Trans_Ct < 20) riskScore += 20;
  if (customer.Income_Category === 'Less than $40K') riskScore += 10;
  return Math.min(riskScore, 100);
};

export const getRiskLevel = (riskScore) => {
  if (riskScore <= 20) return { level: 'Low', color: 'text-green-600 bg-green-100' };
  if (riskScore <= 50) return { level: 'Medium', color: 'text-yellow-600 bg-yellow-100' };
  return { level: 'High', color: 'text-red-600 bg-red-100' };
};

export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency', currency: 'USD', minimumFractionDigits: 0, maximumFractionDigits: 0
  }).format(amount || 0);
};
