import React from 'react';
import { Category } from '../types';

interface CategoryCardProps {
  category: Category;
  onCategoryClick: (category: Category) => void;
}

const CategoryCard: React.FC<CategoryCardProps> = ({ category, onCategoryClick }) => {
  const getIconComponent = (iconName: string) => {
    // Simple icon mapping - in a real app you'd import from lucide-react
    const iconMap: { [key: string]: string } = {
      'Smartphone': '📱',
      'Shirt': '👕',
      'Home': '🏠',
      'Car': '🚗',
      'Briefcase': '💼',
      'Dumbbell': '🏋️',
      'Book': '📚',
      'Building': '🏢'
    };
    return iconMap[iconName] || '📦';
  };

  return (
    <button
      onClick={() => onCategoryClick(category)}
      className="group bg-white rounded-xl p-6 shadow-sm hover:shadow-lg transition-all duration-200 border border-gray-100 hover:border-blue-200 transform hover:scale-105"
    >
      <div className="text-center">
        <div className="text-4xl mb-3 group-hover:scale-110 transition-transform duration-200">
          {getIconComponent(category.icon)}
        </div>
        <h3 className="font-semibold text-gray-900 mb-2">{category.name}</h3>
        <p className="text-sm text-gray-500 capitalize">{category.type}</p>
        {category.subcategories && (
          <p className="text-xs text-gray-400 mt-1">
            {category.subcategories.length} subcategories
          </p>
        )}
      </div>
    </button>
  );
};

export default CategoryCard;