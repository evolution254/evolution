import React from 'react';
import { Clock, X } from 'lucide-react';
import { Product } from '../types';

interface RecentlyViewedProps {
  products: Product[];
  onProductClick: (product: Product) => void;
  onSellerClick: (sellerId: string) => void;
  onClearHistory: () => void;
}

const RecentlyViewed: React.FC<RecentlyViewedProps> = ({
  products,
  onProductClick,
  onSellerClick,
  onClearHistory
}) => {
  if (products.length === 0) return null;

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center space-x-2">
          <Clock className="h-6 w-6 text-gray-600" />
          <h2 className="text-2xl font-bold text-gray-900">Recently Viewed</h2>
        </div>
        <button
          onClick={onClearHistory}
          className="text-gray-500 hover:text-red-600 transition-colors flex items-center space-x-1"
        >
          <X className="h-4 w-4" />
          <span>Clear History</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {products.slice(0, 8).map((product) => (
          <div
            key={product.id}
            className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200 overflow-hidden group cursor-pointer"
            onClick={() => onProductClick(product)}
          >
            <div className="aspect-square overflow-hidden">
              <img
                src={product.images[0]}
                alt={product.title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
              />
            </div>
            
            <div className="p-4">
              <h3 className="font-semibold text-gray-900 line-clamp-2 mb-2">
                {product.title}
              </h3>
              <div className="text-lg font-bold text-blue-600 mb-2">
                {formatPrice(product.price)}
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onSellerClick(product.sellerId);
                }}
                className="text-sm text-gray-600 hover:text-blue-600 transition-colors"
              >
                {product.sellerName}
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default RecentlyViewed;