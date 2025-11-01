'use client'

import { useEffect, useState } from 'react'
import AdminLayout from '@/components/AdminLayout'
import { supabase } from '@/lib/supabase'
import { Leaf, TrendingUp, Calendar } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface CategoryStats {
  category: string
  count: number
}

interface MonthlyData {
  month: string
  [key: string]: number | string
}

const DISEASE_CATEGORIES = [
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

// Color palette for each category
const CATEGORY_COLORS: Record<string, string> = {
  'Healthy': '#10b981',
  'Bacterial Spot': '#ef4444',
  'Early Blight': '#f97316',
  'Late Blight': '#dc2626',
  'Leaf Mold': '#8b5cf6',
  'Septoria Leaf Spot': '#ec4899',
  'Spider Mites': '#f59e0b',
  'Target Spot': '#06b6d4',
  'Mosaic Virus': '#6366f1',
  'Yellow Curl Virus': '#eab308'
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<CategoryStats[]>([])
  const [monthlyData, setMonthlyData] = useState<MonthlyData[]>([])
  const [loading, setLoading] = useState(true)
  const [totalImages, setTotalImages] = useState(0)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setLoading(true)
      
      // Fetch all predictions with timestamps
      const { data, error } = await supabase
        .from('predictions')
        .select('predicted_label, final_label, created_at')
        .order('created_at', { ascending: true })

      if (error) throw error

      // Count by category (use final_label if exists, otherwise predicted_label)
      const counts: Record<string, number> = {}
      
      data?.forEach((item) => {
        const label = item.final_label || item.predicted_label
        counts[label] = (counts[label] || 0) + 1
      })

      // Convert to array and ensure all categories are present
      const statsArray = DISEASE_CATEGORIES.map(category => ({
        category,
        count: counts[category] || 0
      }))

      setStats(statsArray)
      setTotalImages(data?.length || 0)

      // Process monthly data
      const monthlyStats: Record<string, Record<string, number>> = {}
      
      data?.forEach((item) => {
        const label = item.final_label || item.predicted_label
        const date = new Date(item.created_at)
        const monthKey = date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' })
        
        if (!monthlyStats[monthKey]) {
          monthlyStats[monthKey] = {}
          DISEASE_CATEGORIES.forEach(cat => {
            monthlyStats[monthKey][cat] = 0
          })
        }
        
        monthlyStats[monthKey][label] = (monthlyStats[monthKey][label] || 0) + 1
      })

      // Convert to array format for recharts
      const monthlyArray: MonthlyData[] = Object.entries(monthlyStats).map(([month, categories]) => ({
        month,
        ...categories
      }))

      setMonthlyData(monthlyArray)
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

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
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Overview of tomato leaf disease dataset</p>
        </div>

        {/* Total Images Card */}
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm font-medium">Total Images</p>
              <h2 className="text-4xl font-bold mt-2">{totalImages.toLocaleString()}</h2>
            </div>
            <div className="bg-white/20 p-4 rounded-lg">
              <Leaf className="w-8 h-8" />
            </div>
          </div>
        </div>

        {/* Monthly Analysis Bar Chart */}
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-3 mb-6">
            <div className="bg-green-100 p-3 rounded-lg">
              <Calendar className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Monthly Analysis</h2>
              <p className="text-sm text-gray-600">Tomato leaf disease detection trends over time</p>
            </div>
          </div>
          
          <div className="w-full h-[500px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={monthlyData}
                margin={{ top: 20, right: 30, left: 20, bottom: 80 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="month" 
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  tick={{ fill: '#6b7280', fontSize: 12 }}
                />
                <YAxis 
                  tick={{ fill: '#6b7280', fontSize: 12 }}
                  label={{ value: 'Number of Images', angle: -90, position: 'insideLeft', style: { fill: '#6b7280' } }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                  }}
                />
                <Legend 
                  wrapperStyle={{ paddingTop: '20px' }}
                  iconType="square"
                />
                {DISEASE_CATEGORIES.map((category) => (
                  <Bar 
                    key={category}
                    dataKey={category} 
                    fill={CATEGORY_COLORS[category]}
                    radius={[4, 4, 0, 0]}
                  />
                ))}
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Category Stats Grid */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Images by Category</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {stats.map((stat) => (
              <div
                key={stat.category}
                className="bg-white rounded-lg p-5 border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-600">{stat.category}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stat.count}</p>
                  </div>
                  <div className={`p-2 rounded-lg ${
                    stat.category === 'Healthy' 
                      ? 'bg-green-100 text-green-600' 
                      : 'bg-red-100 text-red-600'
                  }`}>
                    <TrendingUp className="w-5 h-5" />
                  </div>
                </div>
                <div className="mt-3 pt-3 border-t border-gray-100">
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>Percentage</span>
                    <span className="font-medium">
                      {totalImages > 0 ? ((stat.count / totalImages) * 100).toFixed(1) : 0}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </AdminLayout>
  )
}

