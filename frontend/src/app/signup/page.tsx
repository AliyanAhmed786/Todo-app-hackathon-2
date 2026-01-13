import SignupFormClient from '../../components/SignupFormClient';

export default function SignupPage() {
  return <SignupFormClient />;
}

// Metadata export for the signup page
export async function generateMetadata() {
  return {
    title: 'Sign Up - Todo App',
    description: 'Create your account to start managing your tasks',
  };
}
