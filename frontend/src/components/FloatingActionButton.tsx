import React from 'react';
import { Plus } from 'lucide-react';

interface FloatingActionButtonProps {
  onSellClick: () => void;
}

const FloatingActionButton: React.FC<FloatingActionButtonProps> = ({ onSellClick }) => {
  return (
    <button
      onClick={onSellClick}
      className="fixed bottom-6 right-6 bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-700 hover:to-emerald-700 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-110 z-40"
      aria-label="Sell Item"
    >
      <Plus className="h-6 w-6" />
    </button>
  );
};

export default FloatingActionButton;