// Sample customer data based on the raw_BankChurners.csv structure
// In a real application, this would fetch data from an API endpoint
export const generateCustomerData = () => {
  const customers = [];
  
  // Sample data representing the structure from raw_BankChurners.csv
  const sampleCustomers = [
    {
      CLIENTNUM: 768805383,
      Attrition_Flag: "Existing Customer",
      Customer_Age: 45,
      Gender: "M",
      Dependent_count: 3,
      Education_Level: "High School",
      Marital_Status: "Married",
      Income_Category: "$60K - $80K",
      Card_Category: "Blue",
      Months_on_book: 39,
      Total_Relationship_Count: 5,
      Months_Inactive_12_mon: 1,
      Contacts_Count_12_mon: 3,
      Credit_Limit: 12691,
      Total_Revolving_Bal: 777,
      Avg_Open_To_Buy: 11914,
      Total_Trans_Amt: 1144,
      Total_Trans_Ct: 42,
      Avg_Utilization_Ratio: 0.061
    },
    {
      CLIENTNUM: 818770008,
      Attrition_Flag: "Existing Customer",
      Customer_Age: 49,
      Gender: "F",
      Dependent_count: 5,
      Education_Level: "Graduate",
      Marital_Status: "Single",
      Income_Category: "Less than $40K",
      Card_Category: "Blue",
      Months_on_book: 44,
      Total_Relationship_Count: 6,
      Months_Inactive_12_mon: 1,
      Contacts_Count_12_mon: 2,
      Credit_Limit: 8256,
      Total_Revolving_Bal: 864,
      Avg_Open_To_Buy: 7392,
      Total_Trans_Amt: 1291,
      Total_Trans_Ct: 33,
      Avg_Utilization_Ratio: 0.105
    },
    {
      CLIENTNUM: 713982108,
      Attrition_Flag: "Existing Customer",
      Customer_Age: 51,
      Gender: "M",
      Dependent_count: 3,
      Education_Level: "Graduate",
      Marital_Status: "Married",
      Income_Category: "$80K - $120K",
      Card_Category: "Blue",
      Months_on_book: 36,
      Total_Relationship_Count: 4,
      Months_Inactive_12_mon: 1,
      Contacts_Count_12_mon: 0,
      Credit_Limit: 3418,
      Total_Revolving_Bal: 0,
      Avg_Open_To_Buy: 3418,
      Total_Trans_Amt: 1887,
      Total_Trans_Ct: 20,
      Avg_Utilization_Ratio: 0
    },
    {
      CLIENTNUM: 769911858,
      Attrition_Flag: "Existing Customer",
      Customer_Age: 40,
      Gender: "F",
      Dependent_count: 4,
      Education_Level: "High School",
      Marital_Status: "Unknown",
      Income_Category: "Less than $40K",
      Card_Category: "Blue",
      Months_on_book: 34,
      Total_Relationship_Count: 3,
      Months_Inactive_12_mon: 4,
      Contacts_Count_12_mon: 1,
      Credit_Limit: 3313,
      Total_Revolving_Bal: 2517,
      Avg_Open_To_Buy: 796,
      Total_Trans_Amt: 1171,
      Total_Trans_Ct: 20,
      Avg_Utilization_Ratio: 0.76
    },
    {
      CLIENTNUM: 860181079,
      Attrition_Flag: "Attrited Customer",
      Customer_Age: 42,
      Gender: "M",
      Dependent_count: 2,
      Education_Level: "Graduate",
      Marital_Status: "Married",
      Income_Category: "$40K - $60K",
      Card_Category: "Silver",
      Months_on_book: 25,
      Total_Relationship_Count: 2,
      Months_Inactive_12_mon: 6,
      Contacts_Count_12_mon: 4,
      Credit_Limit: 5500,
      Total_Revolving_Bal: 1200,
      Avg_Open_To_Buy: 4300,
      Total_Trans_Amt: 850,
      Total_Trans_Ct: 15,
      Avg_Utilization_Ratio: 0.22
    }
  ];

  // Generate more sample customers based on the patterns
  for (let i = 0; i < 100; i++) {
    const baseCustomer = sampleCustomers[i % sampleCustomers.length];
    const customer = {
      ...baseCustomer,
      CLIENTNUM: baseCustomer.CLIENTNUM + i,
      Customer_Age: Math.floor(Math.random() * 40) + 25, // Age 25-65
      Attrition_Flag: Math.random() > 0.16 ? "Existing Customer" : "Attrited Customer", // 16% churn rate
      Credit_Limit: Math.floor(Math.random() * 30000) + 2000,
      Total_Trans_Amt: Math.floor(Math.random() * 5000) + 500,
      Total_Trans_Ct: Math.floor(Math.random() * 100) + 10,
      Avg_Utilization_Ratio: Math.random() * 0.8
    };
    customers.push(customer);
  }

  return customers;
};

// Calculate churn risk based on customer attributes
export const calculateChurnRisk = (customer) => {
  let riskScore = 0;
  
  // Age factor
  if (customer.Customer_Age > 60) riskScore += 10;
  else if (customer.Customer_Age < 30) riskScore += 15;
  
  // Inactivity factor
  if (customer.Months_Inactive_12_mon > 3) riskScore += 20;
  
  // Contact frequency factor
  if (customer.Contacts_Count_12_mon > 4) riskScore += 15;
  
  // Utilization ratio factor
  if (customer.Avg_Utilization_Ratio > 0.7) riskScore += 25;
  else if (customer.Avg_Utilization_Ratio < 0.1) riskScore += 10;
  
  // Transaction activity factor
  if (customer.Total_Trans_Ct < 20) riskScore += 20;
  
  // Income category factor
  if (customer.Income_Category === "Less than $40K") riskScore += 10;
  
  return Math.min(riskScore, 100); // Cap at 100%
};

// Get risk level color
export const getRiskLevel = (riskScore) => {
  if (riskScore <= 20) return { level: 'Low', color: 'text-green-600 bg-green-100' };
  if (riskScore <= 50) return { level: 'Medium', color: 'text-yellow-600 bg-yellow-100' };
  return { level: 'High', color: 'text-red-600 bg-red-100' };
};

// Format currency
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};
