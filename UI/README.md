# Customer Churn Dashboard

A modern, responsive React dashboard for analyzing customer churn patterns and risk assessment.

## Features

### Dashboard View
- **KPI Cards**: Display key metrics including risky customers, impacted revenue, and churn rates
- **Outcomes by Status**: Stacked bar chart showing customer status distribution over time
- **Churn Risk by Income**: Histogram showing spending patterns across churn risk percentiles
- **Segment Analysis**: Bubble chart identifying which customer segments are likely to leave
- **Location Mapping**: Geographic visualization of churn risk by location
- **Customer Table**: Detailed customer information with risk assessment and actions

### Customer List View
- **Complete Customer Database**: Full customer information based on raw bank churn data
- **Advanced Filtering**: Filter by risk level, customer status, and search functionality
- **Detailed Customer Profiles**: Demographics, financial info, activity metrics, and churn risk
- **Real-time Risk Assessment**: Calculated churn risk based on customer behavior patterns
- **Export Functionality**: Download customer data as CSV
- **Responsive Design**: Optimized for desktop, tablet, and mobile viewing

### Navigation
- **Sidebar Navigation**: Easy switching between Dashboard and Customer List views
- **Mobile-Friendly**: Collapsible sidebar for mobile devices
- **Quick Stats**: Summary statistics in the sidebar

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Navigate to the UI directory:
```bash
cd UI
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open [http://localhost:3000](http://localhost:3000) to view the dashboard in your browser.

## Project Structure

```
UI/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Dashboard.js          # Main dashboard layout
│   │   ├── KPICards.js          # Key performance indicator cards
│   │   ├── OutcomesByStatus.js   # Monthly outcomes bar chart
│   │   ├── ChurnRiskByIncome.js # Income-based churn risk histogram
│   │   ├── SegmentsAnalysis.js  # Customer segments bubble chart
│   │   ├── ChurnRiskByLocation.js # Geographic churn analysis
│   │   └── CustomerTable.js      # Customer details table
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
├── tailwind.config.js
└── README.md
```

## Technologies Used

- **React 18**: Frontend framework
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Recharts**: Chart library for data visualization
- **Lucide React**: Icon library

## Available Scripts

- `npm start`: Runs the app in development mode
- `npm build`: Builds the app for production
- `npm test`: Launches the test runner
- `npm eject`: Ejects from Create React App (one-way operation)

## Data Integration

The dashboard currently uses sample data for demonstration purposes. To integrate with real data:

1. Replace sample data in components with API calls to your backend
2. Update the data processing logic to match your data structure
3. Add loading states and error handling for API requests

## Customization

- Modify colors and styling in `tailwind.config.js`
- Update chart configurations in individual component files
- Add new KPI cards by extending the `KPICards.js` component
- Customize the layout by modifying `Dashboard.js`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
