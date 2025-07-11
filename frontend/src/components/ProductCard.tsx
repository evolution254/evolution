import React from 'react';
import { Heart, Eye, MapPin, Star, Zap } from 'lucide-react';
import { Product } from '../types';

interface ProductCardProps {
  product: Product;
  onProductClick: (product: Product) => void;
  onSellerClick: (sellerId: string) => void;
  onAddToCompare?: (product: Product) => void;
  isInCompareList?: boolean;
  showCompareButton?: boolean;
}

const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onProductClick,
  onSellerClick,
  onAddToCompare,
  isInCompareList = false,
  showCompareButton = false
}) => {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const getConditionColor = (condition: string) => {
    switch (condition) {
      case 'new':
        return 'bg-green-100 text-green-800';
      case 'used':
        return 'bg-yellow-100 text-yellow-800';
      case 'refurbished':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-200 border border-gray-100 hover:border-blue-200 overflow-hidden group">
      {/* Image */}
      <div className="relative aspect-square overflow-hidden">
        <img
          src={product.images[0] || 'https://images.pexels.com/photos/230544/pexels-photo-230544.jpeg?auto=compress&cs=tinysrgb&w=500'}
          alt={product.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200 cursor-pointer"
          onClick={() => onProductClick(product)}
        />
        
        {/* Badges */}
        <div className="absolute top-3 left-3 flex flex-col space-y-2">
          {product.isBoosted && (
            <span className="bg-yellow-500 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1">
              <Zap className="h-3 w-3" />
              <span>Boosted</span>
            </span>
          )}
          <span className={`px-2 py-1 rounded-full text-xs font-medium capitalize ${getConditionColor(product.condition)}`}>
            {product.condition}
          </span>
        </div>

        {/* Favorite Button */}
        <button className="absolute top-3 right-3 p-2 bg-white/80 backdrop-blur-sm rounded-full hover:bg-white transition-colors">
          <Heart className="h-4 w-4 text-gray-600 hover:text-red-500" />
        </button>

        {/* Stats */}
        <div className="absolute bottom-3 right-3 flex items-center space-x-2">
          <div className="bg-black/50 backdrop-blur-sm text-white px-2 py-1 rounded-full text-xs flex items-center space-x-1">
            <Eye className="h-3 w-3" />
            <span>{product.views}</span>
          </div>
          <div className="bg-black/50 backdrop-blur-sm text-white px-2 py-1 rounded-full text-xs flex items-center space-x-1">
            <Heart className="h-3 w-3" />
            <span>{product.likes}</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <div className="mb-2">
          <h3 
            className="font-semibold text-gray-900 line-clamp-2 cursor-pointer hover:text-blue-600 transition-colors"
            onClick={() => onProductClick(product)}
          >
            {product.title}
          </h3>
          <p className="text-2xl font-bold text-blue-600 mt-1">
            {formatPrice(product.price)}
          </p>
        </div>

        {/* Location */}
        {product.location && (
          <div className="flex items-center space-x-1 text-gray-500 text-sm mb-3">
            <MapPin className="h-4 w-4" />
            <span>{product.location}</span>
          </div>
        )}

        {/* Seller Info */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => onSellerClick(product.sellerId)}
            className="flex items-center space-x-2 hover:text-blue-600 transition-colors"
          >
            <div className="h-8 w-8 bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full flex items-center justify-center text-white text-sm font-medium">
              {product.sellerName.charAt(0).toUpperCase()}
            </div>
            <div className="text-left">
              <p className="text-sm font-medium text-gray-900">{product.sellerName}</p>
              <div className="flex items-center space-x-1">
                <Star className="h-3 w-3 text-yellow-500 fill-current" />
                <span className="text-xs text-gray-500">{product.sellerRating}</span>
              </div>
            </div>
          </button>

          {showCompareButton && onAddToCompare && (
            <button
              onClick={() => onAddToCompare(product)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                isInCompareList
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-blue-100 hover:text-blue-700'
              }`}
            >
              {isInCompareList ? 'Added' : 'Compare'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;