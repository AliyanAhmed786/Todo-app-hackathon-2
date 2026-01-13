import LoginFormClient from '../../components/LoginFormClient';

export default function LoginPage() {
  return <LoginFormClient />;
}

// Metadata export for the login page
export async function generateMetadata() {
  return {
    title: 'Sign In - Todo App',
    description: 'Sign in to access your account and manage your tasks',
  };
}
