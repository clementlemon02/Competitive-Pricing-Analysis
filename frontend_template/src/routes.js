import React from 'react'

const Overview = React.lazy(() => import('./views/overview/Overview'))
const Revenue = React.lazy(() => import('./views/revenue/Revenue'))
const Tourism = React.lazy(() => import('./views/tourism/Tourism'))
const Price_simulation = React.lazy(() => import('./views/price_simulation/Price_simulation'))
const Occupancy_rate = React.lazy(() => import('./views/occupancy_rate/Occupancy_rate'))
const Competitor_price = React.lazy(() => import('./views/competitor_price/Competitor_price'))

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'))

const DocsCallout = React.lazy(() => import('./components/DocsCallout'))
const DocsExample = React.lazy(() => import('./components/DocsExample'))
const Docslink = React.lazy(() => import('./components/DocsLink'))

const Charts = React.lazy(() => import('./views/charts/Charts'))

// Icons
const CoreUIIcons = React.lazy(() => import('./views/icons/coreui-icons/CoreUIIcons'))
const Flags = React.lazy(() => import('./views/icons/flags/Flags'))
const Brands = React.lazy(() => import('./views/icons/brands/Brands'))
const Widgets = React.lazy(() => import('./views/widgets/Widgets'))

const routes = [
  { path: '/', exact: true, name: 'Home' },
  { path: '/', name: 'Dashboard', element: Dashboard },
  { path: '/dashboard', name: 'Dashboard', element: Dashboard },
  { path: '/dashboard', name: 'Dashboard', element: Dashboard },
  { path: '/dashboard', name: 'Dashboard', element: Dashboard },
  { path: '/overview', name: 'Overview', element: Overview },
  { path: '/charts', name: 'Charts', element: Charts },
  { path: '/revenue', name: 'Revenue', element: Revenue },
  { path: '/tourism', name: 'Tourism', element: Tourism },
  { path: '/price_simulation', name: 'Price_simulation', element: Price_simulation },
  { path: '/occupancy_rate', name: 'Occupancy_rate', element: Occupancy_rate },
  { path: '/competitor_price', name: 'Competitor_price', element: Competitor_price },
  { path: '/icons', exact: true, name: 'Icons', element: CoreUIIcons },
  { path: '/icons/coreui-icons', name: 'CoreUI Icons', element: CoreUIIcons },
  { path: '/icons/flags', name: 'Flags', element: Flags },
  { path: '/icons/brands', name: 'Brands', element: Brands },
  { path: '/widgets', name: 'Widgets', element: Widgets },
]

export default routes
