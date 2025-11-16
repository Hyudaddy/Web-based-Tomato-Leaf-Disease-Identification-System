'use client'

import { useEffect, useState } from 'react'
import AdminLayout from '@/components/AdminLayout'
import { supabase } from '@/lib/supabase'
import { Leaf, TrendingUp, Calendar, Activity } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts'

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
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-2 border-[#47f793] border-t-transparent mx-auto"></div>
            <p className="mt-4 text-gray-600 font-medium">Loading dashboard...</p>
          </div>
        </div>
      </AdminLayout>
    )
  }

  return (
    <AdminLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1 text-sm">Overview of tomato leaf disease predictions</p>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Total Predictions */}
          <div>
            <p className="text-gray-600 text-sm font-medium mb-2">Total Predictions</p>
            <h2 className="text-5xl font-bold text-gray-900">{totalImages.toLocaleString()}</h2>
            <p className="text-[#47f793] text-sm font-semibold mt-2">Healthy & Diseased</p>
          </div>

          {/* Disease Categories */}
          <div>
            <p className="text-gray-600 text-sm font-medium mb-2">Disease Categories</p>
            <h2 className="text-5xl font-bold text-gray-900">{DISEASE_CATEGORIES.length}</h2>
            <p className="text-gray-600 text-sm font-semibold mt-2">Tracked</p>
          </div>
        </div>

        {/* Monthly Analysis Chart */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Monthly Analysis</h2>
          <div className="w-full h-[400px] border border-gray-200 rounded-lg p-6 bg-white">
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
                  label={{ value: 'Count', angle: -90, position: 'insideLeft', style: { fill: '#6b7280' } }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
                  }}
                />
                <Legend wrapperStyle={{ paddingTop: '20px' }} iconType="square" />
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

        {/* Category Stats */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Predictions by Category</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {stats.map((stat) => (
              <div key={stat.category} className="space-y-3">
                <div className="flex items-center justify-between">
                  <p className="text-gray-700 font-medium">{stat.category}</p>
                  <span className="text-sm font-semibold text-[#47f793]">
                    {totalImages > 0 ? ((stat.count / totalImages) * 100).toFixed(1) : 0}%
                  </span>
                </div>
                <div className="flex items-baseline gap-2">
                  <p className="text-2xl font-bold text-gray-900">{stat.count}</p>
                </div>
                <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-[#47f793] transition-all duration-500"
                    style={{ width: `${totalImages > 0 ? (stat.count / totalImages) * 100 : 0}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </AdminLayout>
  )
}

