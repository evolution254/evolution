import React from 'react';
import { Users, Package, Star, TrendingUp } from 'lucide-react';

const QuickStats: React.FC = () => {
  const stats = [
    {
      icon: Users,
      value: '50K+',
      label: 'Active Users',
      color: 'text-blue-600'
    },
    {
      icon: Package,
      value: '100K+',
      label: 'Products Listed',
      color: 'text-emerald-600'
    },
    {
      icon: Star,
      value: '4.9',
      label: 'Average Rating',
      color: 'text-yellow-600'
    },
    {
      icon: TrendingUp,
      value: '25K+',
      label: 'Successful Sales',
      color: 'text-purple-600'
    }
  ];

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
        {stats.map((stat, index) => (
          <div key={index} className="text-center">
            <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100 mb-4 ${stat.color}`}>
              <stat.icon className="h-6 w-6" />
            </div>
            <div className="text-2xl md:text-3xl font-bold text-gray-900 mb-1">
              {stat.value}
            </div>
            <div className="text-sm md:text-base text-gray-600">
              {stat.label}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default QuickStats;