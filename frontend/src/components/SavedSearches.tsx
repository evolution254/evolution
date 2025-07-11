import React, { useState } from 'react';
import { X, Search, Bell, Trash2, Plus } from 'lucide-react';

interface SavedSearch {
  id: string;
  query: string;
  filters: any;
  notifications: boolean;
  createdAt: string;
}

interface SavedSearchesProps {
  isOpen: boolean;
  onClose: () => void;
}

const SavedSearches: React.FC<SavedSearchesProps> = ({ isOpen, onClose }) => {
  const [savedSearches, setSavedSearches] = useState<SavedSearch[]>([
    {
      id: '1',
      query: 'iPhone 15',
      filters: { category: 'Electronics', maxPrice: 1200 },
      notifications: true,
      createdAt: '2024-01-15T10:00:00Z'
    },
    {
      id: '2',
      query: 'Gaming Chair',
      filters: { category: 'Furniture', condition: 'new' },
      notifications: false,
      createdAt: '2024-01-14T15:30:00Z'
    }
  ]);

  if (!isOpen) return null;

  const toggleNotifications = (id: string) => {
    setSavedSearches(searches =>
      searches.map(search =>
        search.id === id ? { ...search, notifications: !search.notifications } : search
      )
    );
  };

  const deleteSearch = (id: string) => {
    setSavedSearches(searches => searches.filter(search => search.id !== id));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Saved Searches</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {savedSearches.length === 0 ? (
          <div className="p-12 text-center">
            <div className="text-gray-400 mb-4">
              <Search className="h-16 w-16 mx-auto" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No saved searches</h3>
            <p className="text-gray-500 mb-6">Save your searches to get notified when new items match your criteria.</p>
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2 mx-auto">
              <Plus className="h-4 w-4" />
              <span>Create Search Alert</span>
            </button>
          </div>
        ) : (
          <div className="p-6">
            <div className="space-y-4">
              {savedSearches.map((search) => (
                <div key={search.id} className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <Search className="h-4 w-4 text-gray-500" />
                        <h3 className="font-semibold text-gray-900">{search.query}</h3>
                      </div>
                      
                      <div className="text-sm text-gray-600 mb-3">
                        <div className="flex flex-wrap gap-2">
                          {Object.entries(search.filters).map(([key, value]) => (
                            <span key={key} className="bg-white px-2 py-1 rounded text-xs">
                              {key}: {value}
                            </span>
                          ))}
                        </div>
                      </div>
                      
                      <div className="text-xs text-gray-500">
                        Created {new Date(search.createdAt).toLocaleDateString()}
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => toggleNotifications(search.id)}
                        className={`p-2 rounded-full transition-colors ${
                          search.notifications
                            ? 'bg-blue-100 text-blue-600'
                            : 'bg-gray-200 text-gray-500'
                        }`}
                        title={search.notifications ? 'Notifications enabled' : 'Notifications disabled'}
                      >
                        <Bell className="h-4 w-4" />
                      </button>
                      
                      <button
                        onClick={() => deleteSearch(search.id)}
                        className="p-2 bg-red-100 text-red-600 rounded-full hover:bg-red-200 transition-colors"
                        title="Delete search"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3 mt-3">
                    <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                      Run Search
                    </button>
                    <button className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                      Edit
                    </button>
                  </div>
                </div>
              ))}
            </div>
            
            <button className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>Create New Search Alert</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SavedSearches;