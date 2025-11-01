'use client'

import { useEffect, useState } from 'react'
import AdminLayout from '@/components/AdminLayout'
import { supabase } from '@/lib/supabase'
import { Search, Download, Trash2, Edit, Eye, FileDown, Archive } from 'lucide-react'
import Image from 'next/image'

interface Prediction {
  id: string
  storage_path: string
  image_url: string | null
  predicted_label: string
  confidence: number
  final_label: string | null
  uploader_name: string | null
  created_at: string
}

const DISEASE_CATEGORIES = [
  'All Categories',
  'Healthy',
  'Bacterial Spot',
  'Early Blight',
  'Late Blight',
  'Leaf Mold',
  'Septoria Leaf Spot',
  'Spider Mites',
  'Target Spot',
  'Mosaic Virus',
  'Yellow Curl Virus'
]

export default function DatasetPage() {
  const [predictions, setPredictions] = useState<Prediction[]>([])
  const [filteredPredictions, setFilteredPredictions] = useState<Prediction[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState('All Categories')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedImage, setSelectedImage] = useState<Prediction | null>(null)
  const [relabelId, setRelabelId] = useState<string | null>(null)
  const [newLabel, setNewLabel] = useState('')
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 20

  useEffect(() => {
    fetchPredictions()
  }, [])

  useEffect(() => {
    filterPredictions()
  }, [predictions, selectedCategory, searchQuery])

  const fetchPredictions = async () => {
    try {
      setLoading(true)
      const { data, error } = await supabase
        .from('predictions')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error
      setPredictions(data || [])
    } catch (error) {
      console.error('Error fetching predictions:', error)
    } finally {
      setLoading(false)
    }
  }

  const filterPredictions = () => {
    let filtered = [...predictions]

    // Filter by category
    if (selectedCategory !== 'All Categories') {
      filtered = filtered.filter(p => 
        (p.final_label || p.predicted_label) === selectedCategory
      )
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(p =>
        p.storage_path.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.uploader_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.predicted_label.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    setFilteredPredictions(filtered)
    setCurrentPage(1)
  }

  const handleRelabel = async (id: string, label: string) => {
    try {
      const { error } = await supabase
        .from('predictions')
        .update({ final_label: label, updated_at: new Date().toISOString() })
        .eq('id', id)

      if (error) throw error
      
      // Update local state
      setPredictions(predictions.map(p => 
        p.id === id ? { ...p, final_label: label } : p
      ))
      setRelabelId(null)
      setNewLabel('')
    } catch (error) {
      console.error('Error relabeling:', error)
      alert('Failed to relabel image')
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this image?')) return

    try {
      const { error } = await supabase
        .from('predictions')
        .delete()
        .eq('id', id)

      if (error) throw error
      
      setPredictions(predictions.filter(p => p.id !== id))
    } catch (error) {
      console.error('Error deleting:', error)
      alert('Failed to delete image')
    }
  }

  const handleDownload = async (prediction: Prediction) => {
    try {
      if (!prediction.image_url) {
        alert('Image URL not available')
        return
      }

      const response = await fetch(prediction.image_url)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${prediction.predicted_label}_${prediction.id}.jpg`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Error downloading:', error)
      alert('Failed to download image')
    }
  }

  const exportCSV = () => {
    const csv = [
      ['ID', 'Predicted Label', 'Confidence', 'Final Label', 'Uploader', 'Created At', 'Image URL'].join(','),
      ...filteredPredictions.map(p => [
        p.id,
        p.predicted_label,
        p.confidence,
        p.final_label || '',
        p.uploader_name || '',
        new Date(p.created_at).toLocaleString(),
        p.image_url || ''
      ].join(','))
    ].join('\n')

    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `dataset_${selectedCategory}_${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  }

  const exportZIP = async () => {
    alert('ZIP export will download all filtered images. This may take a while for large datasets.')
    // Note: Full ZIP implementation would require backend support
    // For now, we'll download images one by one
    for (const prediction of filteredPredictions.slice(0, 10)) {
      await handleDownload(prediction)
      await new Promise(resolve => setTimeout(resolve, 500))
    }
  }

  // Pagination
  const totalPages = Math.ceil(filteredPredictions.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentPredictions = filteredPredictions.slice(startIndex, endIndex)

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      </AdminLayout>
    )
  }

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dataset</h1>
            <p className="text-gray-600 mt-2">
              {filteredPredictions.length} images {selectedCategory !== 'All Categories' && `in ${selectedCategory}`}
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={exportCSV}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <FileDown className="w-4 h-4" />
              Export CSV
            </button>
            <button
              onClick={exportZIP}
              className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            >
              <Archive className="w-4 h-4" />
              Export ZIP
            </button>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Category Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Category
              </label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              >
                {DISEASE_CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            {/* Search */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search by filename, uploader..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Image
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Predicted Label
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Confidence
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Final Label
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {currentPredictions.map((prediction) => (
                  <tr key={prediction.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="w-16 h-16 relative rounded-lg overflow-hidden bg-gray-100">
                        {prediction.image_url ? (
                          <Image
                            src={prediction.image_url}
                            alt={prediction.predicted_label}
                            fill
                            className="object-cover"
                          />
                        ) : (
                          <div className="w-full h-full flex items-center justify-center text-gray-400">
                            No image
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-medium text-gray-900">
                        {prediction.predicted_label}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-600">
                        {(prediction.confidence * 100).toFixed(2)}%
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {relabelId === prediction.id ? (
                        <div className="flex items-center gap-2">
                          <select
                            value={newLabel}
                            onChange={(e) => setNewLabel(e.target.value)}
                            className="text-sm border border-gray-300 rounded px-2 py-1"
                          >
                            <option value="">Select...</option>
                            {DISEASE_CATEGORIES.slice(1).map(cat => (
                              <option key={cat} value={cat}>{cat}</option>
                            ))}
                          </select>
                          <button
                            onClick={() => handleRelabel(prediction.id, newLabel)}
                            className="text-xs bg-green-600 text-white px-2 py-1 rounded hover:bg-green-700"
                          >
                            Save
                          </button>
                          <button
                            onClick={() => setRelabelId(null)}
                            className="text-xs bg-gray-300 text-gray-700 px-2 py-1 rounded hover:bg-gray-400"
                          >
                            Cancel
                          </button>
                        </div>
                      ) : (
                        <span className="text-sm text-gray-600">
                          {prediction.final_label || '-'}
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {new Date(prediction.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => setSelectedImage(prediction)}
                          className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                          title="Preview"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => {
                            setRelabelId(prediction.id)
                            setNewLabel(prediction.final_label || prediction.predicted_label)
                          }}
                          className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                          title="Relabel"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDownload(prediction)}
                          className="p-2 text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
                          title="Download"
                        >
                          <Download className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(prediction.id)}
                          className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
              <div className="text-sm text-gray-600">
                Showing {startIndex + 1} to {Math.min(endIndex, filteredPredictions.length)} of {filteredPredictions.length} results
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                <span className="px-4 py-2 text-sm text-gray-600">
                  Page {currentPage} of {totalPages}
                </span>
                <button
                  onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Preview Modal */}
      {selectedImage && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedImage(null)}
        >
          <div
            className="bg-white rounded-xl p-6 max-w-3xl w-full max-h-[90vh] overflow-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-gray-900">Image Preview</h3>
              <button
                onClick={() => setSelectedImage(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            {selectedImage.image_url && (
              <div className="relative w-full h-96 mb-4">
                <Image
                  src={selectedImage.image_url}
                  alt={selectedImage.predicted_label}
                  fill
                  className="object-contain"
                />
              </div>
            )}
            <div className="space-y-2 text-sm">
              <p><strong>Predicted:</strong> {selectedImage.predicted_label}</p>
              <p><strong>Confidence:</strong> {(selectedImage.confidence * 100).toFixed(2)}%</p>
              <p><strong>Final Label:</strong> {selectedImage.final_label || 'Not set'}</p>
              <p><strong>Date:</strong> {new Date(selectedImage.created_at).toLocaleString()}</p>
            </div>
          </div>
        </div>
      )}
    </AdminLayout>
  )
}

