'use client'

import { useEffect, useState } from 'react'
import AdminLayout from '@/components/AdminLayout'
import { supabase } from '@/lib/supabase'
import { TrendingUp, TrendingDown, AlertTriangle, Activity, Calendar, BarChart3, PieChart } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart as RechartsPie, Pie, Cell, Area, AreaChart } from 'recharts'

interface CategoryStats {
  category: string
  count: number
}

interface DailyData {
  date: string
  count: number
  healthy: number
  diseased: number
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

// Green monochrome palette for charts
const GREEN_PALETTE = {
  primary: '#10b981',      // Main green
  light: '#34d399',        // Light green
  lighter: '#6ee7b7',      // Lighter
  lightest: '#a7f3d0',     // Lightest
  dark: '#059669',         // Dark green
  darker: '#047857',       // Darker
  darkest: '#065f46',      // Darkest
  accent: '#022c22',       // Almost black green
  bg: '#ecfdf5',           // Background tint
  border: '#d1fae5'        // Border color
}

// Shades for bar chart (all green variations)
const CATEGORY_SHADES: Record<string, string> = {
  'Healthy': GREEN_PALETTE.primary,
  'Bacterial Spot': GREEN_PALETTE.dark,
  'Early Blight': GREEN_PALETTE.darker,
  'Late Blight': GREEN_PALETTE.darkest,
  'Leaf Mold': GREEN_PALETTE.light,
  'Septoria Leaf Spot': GREEN_PALETTE.lighter,
  'Spider Mites': GREEN_PALETTE.lightest,
  'Target Spot': '#15803d',
  'Mosaic Virus': '#166534',
  'Yellow Curl Virus': '#14532d'
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<CategoryStats[]>([])
  const [monthlyData, setMonthlyData] = useState<MonthlyData[]>([])
  const [dailyTrend, setDailyTrend] = useState<DailyData[]>([])
  const [loading, setLoading] = useState(true)

  // KPI States
  const [totalImages, setTotalImages] = useState(0)
  const [todayCount, setTodayCount] = useState(0)
  const [weekCount, setWeekCount] = useState(0)
  const [avgConfidence, setAvgConfidence] = useState(0)
  const [highRiskCount, setHighRiskCount] = useState(0)
  const [healthyCount, setHealthyCount] = useState(0)
  const [diseasedCount, setDiseasedCount] = useState(0)

  // Trend indicators
  const [weekTrend, setWeekTrend] = useState<'up' | 'down' | 'neutral'>('neutral')
  const [trendPercentage, setTrendPercentage] = useState(0)

  // Disease outbreak detection
  const [outbreakAlerts, setOutbreakAlerts] = useState<string[]>([])

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setLoading(true)

      // Fetch all predictions with timestamps and confidence
      const { data, error } = await supabase
        .from('predictions')
        .select('predicted_label, final_label, created_at, confidence')
        .order('created_at', { ascending: true })

      if (error) throw error

      const now = new Date()
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000)
      const twoWeeksAgo = new Date(today.getTime() - 14 * 24 * 60 * 60 * 1000)

      // Calculate KPIs
      let todayPredictions = 0
      let thisWeekPredictions = 0
      let lastWeekPredictions = 0
      let totalConfidence = 0
      let highRisk = 0
      let healthy = 0
      let diseased = 0

      // Daily trend data (last 30 days)
      const dailyStats: Record<string, { count: number; healthy: number; diseased: number }> = {}
      const last30Days = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000)

      // Disease counts for outbreak detection
      const weeklyDiseaseCounts: Record<string, number> = {}
      const previousWeekDiseaseCounts: Record<string, number> = {}

      // Count by category
      const counts: Record<string, number> = {}

      data?.forEach((item) => {
        const label = item.final_label || item.predicted_label
        const createdDate = new Date(item.created_at)
        const confidence = item.confidence || 0

        // Total counts
        counts[label] = (counts[label] || 0) + 1
        totalConfidence += confidence

        // High risk: low confidence (< 60%) or severe diseases
        if (confidence < 0.6 || ['Late Blight', 'Mosaic Virus', 'Yellow Curl Virus'].includes(label)) {
          highRisk++
        }

        // Healthy vs Diseased
        if (label === 'Healthy') {
          healthy++
        } else {
          diseased++
        }

        // Today's predictions
        if (createdDate >= today) {
          todayPredictions++
        }

        // This week's predictions
        if (createdDate >= weekAgo) {
          thisWeekPredictions++
          if (label !== 'Healthy') {
            weeklyDiseaseCounts[label] = (weeklyDiseaseCounts[label] || 0) + 1
          }
        }

        // Last week's predictions (for trend)
        if (createdDate >= twoWeeksAgo && createdDate < weekAgo) {
          lastWeekPredictions++
          if (label !== 'Healthy') {
            previousWeekDiseaseCounts[label] = (previousWeekDiseaseCounts[label] || 0) + 1
          }
        }

        // Daily trend (last 30 days)
        if (createdDate >= last30Days) {
          const dateKey = createdDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
          if (!dailyStats[dateKey]) {
            dailyStats[dateKey] = { count: 0, healthy: 0, diseased: 0 }
          }
          dailyStats[dateKey].count++
          if (label === 'Healthy') {
            dailyStats[dateKey].healthy++
          } else {
            dailyStats[dateKey].diseased++
          }
        }
      })

      // Set KPI values
      setTodayCount(todayPredictions)
      setWeekCount(thisWeekPredictions)
      setAvgConfidence(data?.length ? (totalConfidence / data.length) * 100 : 0)
      setHighRiskCount(highRisk)
      setHealthyCount(healthy)
      setDiseasedCount(diseased)
      setTotalImages(data?.length || 0)

      // Calculate week-over-week trend
      if (lastWeekPredictions > 0) {
        const change = ((thisWeekPredictions - lastWeekPredictions) / lastWeekPredictions) * 100
        setTrendPercentage(Math.abs(change))
        setWeekTrend(change > 5 ? 'up' : change < -5 ? 'down' : 'neutral')
      }

      // Detect disease outbreaks (>50% increase in any disease)
      const alerts: string[] = []
      Object.keys(weeklyDiseaseCounts).forEach(disease => {
        const current = weeklyDiseaseCounts[disease]
        const previous = previousWeekDiseaseCounts[disease] || 0
        if (previous > 0 && current > previous * 1.5) {
          alerts.push(disease)
        } else if (previous === 0 && current >= 3) {
          alerts.push(disease)
        }
      })
      setOutbreakAlerts(alerts)

      // Convert to array and ensure all categories are present
      const statsArray = DISEASE_CATEGORIES.map(category => ({
        category,
        count: counts[category] || 0
      }))
      setStats(statsArray)

      // Process daily trend data
      const dailyArray = Object.entries(dailyStats)
        .map(([date, values]) => ({ date, ...values }))
        .slice(-14) // Last 14 days
      setDailyTrend(dailyArray)

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

  // Pie chart data for healthy vs diseased
  const healthRatioData = [
    { name: 'Healthy', value: healthyCount, color: GREEN_PALETTE.primary },
    { name: 'Diseased', value: diseasedCount, color: GREEN_PALETTE.darkest }
  ]

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-2 border-emerald-500 border-t-transparent mx-auto"></div>
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
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-500 mt-1">Overview of tomato leaf disease predictions</p>
          </div>
          <div className="text-sm text-gray-500">
            Last updated: {new Date().toLocaleString()}
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Today's Predictions */}
          <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="p-2 bg-emerald-50 rounded-lg">
                <Calendar className="w-5 h-5 text-emerald-600" />
              </div>
              <span className="text-xs font-medium text-gray-400 uppercase tracking-wide">Today</span>
            </div>
            <p className="text-3xl font-bold text-gray-900">{todayCount}</p>
            <p className="text-sm text-gray-500 mt-1">Predictions today</p>
          </div>

          {/* This Week's Predictions */}
          <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="p-2 bg-emerald-50 rounded-lg">
                <BarChart3 className="w-5 h-5 text-emerald-600" />
              </div>
              <div className="flex items-center gap-1">
                {weekTrend === 'up' && <TrendingUp className="w-4 h-4 text-emerald-500" />}
                {weekTrend === 'down' && <TrendingDown className="w-4 h-4 text-gray-400" />}
                {trendPercentage > 0 && (
                  <span className={`text-xs font-medium ${weekTrend === 'up' ? 'text-emerald-500' : 'text-gray-400'}`}>
                    {weekTrend === 'up' ? '+' : '-'}{trendPercentage.toFixed(0)}%
                  </span>
                )}
              </div>
            </div>
            <p className="text-3xl font-bold text-gray-900">{weekCount}</p>
            <p className="text-sm text-gray-500 mt-1">Predictions this week</p>
          </div>

          {/* Average Confidence */}
          <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="p-2 bg-emerald-50 rounded-lg">
                <Activity className="w-5 h-5 text-emerald-600" />
              </div>
              <span className="text-xs font-medium text-gray-400 uppercase tracking-wide">Avg</span>
            </div>
            <p className="text-3xl font-bold text-gray-900">{avgConfidence.toFixed(1)}%</p>
            <p className="text-sm text-gray-500 mt-1">Model confidence</p>
            <div className="mt-3 h-1.5 bg-gray-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-emerald-500 rounded-full transition-all duration-500"
                style={{ width: `${avgConfidence}%` }}
              />
            </div>
          </div>

          {/* High-Risk Alerts */}
          <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className={`p-2 rounded-lg ${highRiskCount > 0 ? 'bg-amber-50' : 'bg-emerald-50'}`}>
                <AlertTriangle className={`w-5 h-5 ${highRiskCount > 0 ? 'text-amber-500' : 'text-emerald-600'}`} />
              </div>
              <span className="text-xs font-medium text-gray-400 uppercase tracking-wide">Alert</span>
            </div>
            <p className="text-3xl font-bold text-gray-900">{highRiskCount}</p>
            <p className="text-sm text-gray-500 mt-1">High-risk predictions</p>
          </div>
        </div>

        {/* Outbreak Alerts */}
        {outbreakAlerts.length > 0 && (
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-amber-500 mt-0.5" />
              <div>
                <p className="font-semibold text-amber-800">Disease Outbreak Detected</p>
                <p className="text-sm text-amber-700 mt-1">
                  Significant increase in: {outbreakAlerts.join(', ')}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Prediction Trend (Area Chart) */}
          <div className="lg:col-span-2 bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">Prediction Trend</h2>
              <span className="text-xs text-gray-400">Last 14 days</span>
            </div>
            <div className="h-[280px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={dailyTrend} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorHealthy" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={GREEN_PALETTE.primary} stopOpacity={0.3} />
                      <stop offset="95%" stopColor={GREEN_PALETTE.primary} stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="colorDiseased" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={GREEN_PALETTE.darkest} stopOpacity={0.3} />
                      <stop offset="95%" stopColor={GREEN_PALETTE.darkest} stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: '#9ca3af', fontSize: 12 }}
                    tickLine={false}
                    axisLine={{ stroke: '#e5e7eb' }}
                  />
                  <YAxis
                    tick={{ fill: '#9ca3af', fontSize: 12 }}
                    tickLine={false}
                    axisLine={false}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#fff',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="healthy"
                    stroke={GREEN_PALETTE.primary}
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorHealthy)"
                    name="Healthy"
                  />
                  <Area
                    type="monotone"
                    dataKey="diseased"
                    stroke={GREEN_PALETTE.darkest}
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorDiseased)"
                    name="Diseased"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Healthy vs Diseased Ratio (Pie Chart) */}
          <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">Health Ratio</h2>
              <PieChart className="w-4 h-4 text-gray-400" />
            </div>
            <div className="h-[200px]">
              <ResponsiveContainer width="100%" height="100%">
                <RechartsPie>
                  <Pie
                    data={healthRatioData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {healthRatioData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#fff',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px'
                    }}
                  />
                </RechartsPie>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-center gap-6 mt-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: GREEN_PALETTE.primary }} />
                <span className="text-sm text-gray-600">Healthy ({healthyCount})</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: GREEN_PALETTE.darkest }} />
                <span className="text-sm text-gray-600">Diseased ({diseasedCount})</span>
              </div>
            </div>
          </div>
        </div>

        {/* Monthly Analysis Chart */}
        <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Monthly Analysis by Category</h2>
            <span className="text-xs text-gray-400">All time</span>
          </div>
          <div className="h-[400px]">
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
                  tick={{ fill: '#9ca3af', fontSize: 12 }}
                  tickLine={false}
                  axisLine={{ stroke: '#e5e7eb' }}
                />
                <YAxis
                  tick={{ fill: '#9ca3af', fontSize: 12 }}
                  tickLine={false}
                  axisLine={false}
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
                  formatter={(value) => <span className="text-sm text-gray-600">{value}</span>}
                />
                {DISEASE_CATEGORIES.map((category) => (
                  <Bar
                    key={category}
                    dataKey={category}
                    fill={CATEGORY_SHADES[category]}
                    radius={[2, 2, 0, 0]}
                  />
                ))}
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Category Stats Grid */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Predictions by Category</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
            {stats.map((stat) => (
              <div
                key={stat.category}
                className="bg-white rounded-xl border border-gray-100 p-4 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between mb-3">
                  <p className="text-sm font-medium text-gray-700 truncate">{stat.category}</p>
                  <span className="text-xs font-semibold text-emerald-600">
                    {totalImages > 0 ? ((stat.count / totalImages) * 100).toFixed(1) : 0}%
                  </span>
                </div>
                <p className="text-2xl font-bold text-gray-900">{stat.count}</p>
                <div className="mt-3 h-1 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-500"
                    style={{
                      width: `${totalImages > 0 ? (stat.count / totalImages) * 100 : 0}%`,
                      backgroundColor: CATEGORY_SHADES[stat.category] || GREEN_PALETTE.primary
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer Stats */}
        <div className="bg-emerald-50 rounded-xl border border-emerald-100 p-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <p className="text-3xl font-bold text-emerald-700">{totalImages.toLocaleString()}</p>
              <p className="text-sm text-emerald-600 mt-1">Total Predictions</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-emerald-700">{DISEASE_CATEGORIES.length}</p>
              <p className="text-sm text-emerald-600 mt-1">Disease Categories</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-emerald-700">
                {totalImages > 0 ? ((healthyCount / totalImages) * 100).toFixed(1) : 0}%
              </p>
              <p className="text-sm text-emerald-600 mt-1">Healthy Rate</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-emerald-700">{avgConfidence.toFixed(0)}%</p>
              <p className="text-sm text-emerald-600 mt-1">Avg Confidence</p>
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
  )
}
