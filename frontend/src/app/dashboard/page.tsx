import { DashboardPageClient } from '../../components/DashboardPageClient';

export default function DashboardPage() {
  return <DashboardPageClient />;
}

// Metadata export for the dashboard page
export async function generateMetadata() {
  return {
    title: 'Dashboard - Todo App',
    description: 'Your personal dashboard to manage tasks and productivity',
  };
}
