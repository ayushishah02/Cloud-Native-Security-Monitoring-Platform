import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Shield, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';

export default function Index() {
  const navigate = useNavigate();
  const { user } = useAuth();

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4">
      <Card className="w-full max-w-lg border-slate-700 bg-slate-800/50 backdrop-blur-sm">
        <CardHeader className="space-y-4 text-center">
          <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-primary/10">
            <Shield className="h-10 w-10 text-primary" />
          </div>
          <div>
            <CardTitle className="text-3xl font-bold text-slate-100">SecureWorks</CardTitle>
            <CardDescription className="mt-2 text-slate-400">
              Enterprise Security Monitoring Demo
            </CardDescription>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          <p className="text-center text-slate-300">
            Welcome to the SecureWorks Demo App — a simulated internal company login portal 
            that generates realistic security event logs for monitoring.
          </p>
          
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-slate-200">Demo Credentials:</h3>
            <div className="space-y-2 rounded-lg border border-slate-600 bg-slate-700/50 p-4">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Standard User:</span>
                <code className="text-slate-200">user@secureworks.demo</code>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Admin User:</span>
                <code className="text-slate-200">admin@secureworks.demo</code>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Passwords:</span>
                <code className="text-slate-200">Password123! / AdminPassword123!</code>
              </div>
            </div>
          </div>

          <Button 
            onClick={() => navigate(user ? '/dashboard' : '/login')}
            className="w-full"
            size="lg"
          >
            {user ? 'Go to Dashboard' : 'Sign In'}
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
