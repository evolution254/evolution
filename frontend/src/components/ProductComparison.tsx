import React from 'react';
import { X, Star, MapPin, Calendar } from 'lucide-react';
import { Product } from '../types';

interface ProductComparisonProps {
  products: Product[];
  isOpen: boolean;
  onClose: () => void;
  onRemoveProduct: (productId: string) => void;
}

const ProductComparison: React.FC<ProductComparisonProps> = ({
  products,
  isOpen,
  onClose,
  onRemoveProduct
}) => {
  if (!isOpen) return null;

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-6xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">
            Compare Products ({products.length})
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {products.length === 0 ? (
          <div className="p-12 text-center">
            <div className="text-gray-400 mb-4">
              <svg className="h-16 w-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No products to compare</h3>
            <p className="text-gray-500">Add products to your comparison list to see them here.</p>
          </div>
        ) : (
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {products.map((product) => (
                <div key={product.id} className="bg-gray-50 rounded-lg p-4 relative">
                  {/* Remove Button */}
                  <button
                    onClick={() => onRemoveProduct(product.id)}
                    className="absolute top-2 right-2 text-gray-400 hover:text-red-500 transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>

                  {/* Product Image */}
                  <div className="aspect-square rounded-lg overflow-hidden mb-4">
                    <img
                      src={product.images[0]}
                      alt={product.title}
                      className="w-full h-full object-cover"
                    />
                  </div>

                  {/* Product Info */}
                  <div className="space-y-3">
                    <h3 className="font-semibold text-gray-900 line-clamp-2">
                      {product.title}
                    </h3>

                    <div className="text-xl font-bold text-blue-600">
                      {formatPrice(product.price)}
                    </div>

                    <div className="space-y-2 text-sm">
                      <div className="flex items-center justify-between">
                        <span className="text-gray-500">Condition:</span>
                        <span className="capitalize font-medium">{product.condition}</span>
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-gray-500">Category:</span>
                        <span className="font-medium">{product.category}</span>
                      </div>

                      {product.location && (
                        <div className="flex items-center justify-between">
                          <span className="text-gray-500">Location:</span>
                          <div className="flex items-center space-x-1">
                            <MapPin className="h-3 w-3" />
                            <span className="font-medium truncate">{product.location}</span>
                          </div>
                        </div>
                      )}

                      <div className="flex items-center justify-between">
                        <span className="text-gray-500">Seller:</span>
                        <div className="flex items-center space-x-1">
                          <Star className="h-3 w-3 text-yellow-500 fill-current" />
                          <span className="font-medium">{product.sellerRating}</span>
                        </div>
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-gray-500">Listed:</span>
                        <div className="flex items-center space-x-1">
                          <Calendar className="h-3 w-3" />
                          <span className="font-medium">
                            {new Date(product.createdAt).toLocaleDateString()}
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-gray-500">Views:</span>
                        <span className="font-medium">{product.views}</span>
                      </div>
                    </div>

                    {/* Action Button */}
                    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors mt-4">
                      View Details
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Comparison Summary */}
            {products.length > 1 && (
              <div className="mt-8 p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-blue-900 mb-2">Quick Comparison</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-blue-700">Price Range:</span>
                    <div className="font-medium">
                      {formatPrice(Math.min(...products.map(p => p.price)))} - {formatPrice(Math.max(...products.map(p => p.price)))}
                    </div>
                  </div>
                  <div>
                    <span className="text-blue-700">Avg. Rating:</span>
                    <div className="font-medium">
                      {(products.reduce((sum, p) => sum + p.sellerRating, 0) / products.length).toFixed(1)}
                    </div>
                  </div>
                  <div>
                    <span className="text-blue-700">Total Views:</span>
                    <div className="font-medium">
                      {products.reduce((sum, p) => sum + p.views, 0).toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <span className="text-blue-700">Categories:</span>
                    <div className="font-medium">
                      {new Set(products.map(p => p.category)).size} unique
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductComparison;