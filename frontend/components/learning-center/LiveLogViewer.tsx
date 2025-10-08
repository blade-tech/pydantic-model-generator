'use client'

/**
 * Live Log Viewer - Learning Center Component
 *
 * Connects to WebSocket endpoint for real-time log streaming.
 * Supports filtering by level, step, and search text.
 */

import { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import {
  Terminal,
  ChevronDown,
  ChevronUp,
  Download,
  Trash2,
  Search,
  Filter
} from 'lucide-react'

interface LogEntry {
  timestamp: string
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL'
  logger: string
  message: string
  module: string
  function: string
  line: number
  step?: number
}

interface LiveLogViewerProps {
  maxHeight?: string
  initialExpanded?: boolean
}

const LEVEL_COLORS = {
  DEBUG: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200',
  INFO: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  WARNING: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  ERROR: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  CRITICAL: 'bg-red-200 text-red-900 dark:bg-red-800 dark:text-red-100'
}

export default function LiveLogViewer({
  maxHeight = '400px',
  initialExpanded = false
}: LiveLogViewerProps) {
  const [isExpanded, setIsExpanded] = useState(initialExpanded)
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [filteredLogs, setFilteredLogs] = useState<LogEntry[]>([])
  const [searchText, setSearchText] = useState('')
  const [levelFilter, setLevelFilter] = useState<string>('all')
  const [stepFilter, setStepFilter] = useState<number | 'all'>('all')
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const wsRef = useRef<WebSocket | null>(null)
  const scrollRef = useRef<HTMLDivElement>(null)
  const autoScrollRef = useRef(true)

  // Connect to WebSocket
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        const ws = new WebSocket('ws://localhost:8000/api/learning-center/logs/stream')

        ws.onopen = () => {
          console.log('WebSocket connected')
          setIsConnected(true)
          setError(null)
        }

        ws.onmessage = (event) => {
          try {
            const logEntry: LogEntry = JSON.parse(event.data)

            // Skip system messages
            if ('type' in logEntry && logEntry.type === 'system') {
              return
            }

            setLogs((prev) => [...prev, logEntry])
          } catch (err) {
            console.error('Failed to parse log entry:', err)
          }
        }

        ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          setError('WebSocket connection error')
        }

        ws.onclose = () => {
          console.log('WebSocket disconnected')
          setIsConnected(false)

          // Attempt to reconnect after 3 seconds
          setTimeout(() => {
            if (wsRef.current?.readyState === WebSocket.CLOSED) {
              console.log('Attempting to reconnect...')
              connectWebSocket()
            }
          }, 3000)
        }

        wsRef.current = ws
      } catch (err) {
        console.error('Failed to create WebSocket:', err)
        setError('Failed to connect to log stream')
      }
    }

    connectWebSocket()

    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  // Apply filters
  useEffect(() => {
    let filtered = logs

    // Level filter
    if (levelFilter !== 'all') {
      filtered = filtered.filter((log) => log.level === levelFilter)
    }

    // Step filter
    if (stepFilter !== 'all') {
      filtered = filtered.filter((log) => log.step === stepFilter)
    }

    // Search filter
    if (searchText.trim()) {
      const search = searchText.toLowerCase()
      filtered = filtered.filter(
        (log) =>
          log.message.toLowerCase().includes(search) ||
          log.module.toLowerCase().includes(search) ||
          log.function.toLowerCase().includes(search)
      )
    }

    setFilteredLogs(filtered)
  }, [logs, searchText, levelFilter, stepFilter])

  // Auto-scroll to bottom
  useEffect(() => {
    if (autoScrollRef.current && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [filteredLogs])

  const handleClearLogs = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/learning-center/logs/clear', {
        method: 'POST'
      })

      if (response.ok) {
        setLogs([])
        setFilteredLogs([])
      }
    } catch (err) {
      console.error('Failed to clear logs:', err)
    }
  }

  const handleDownloadLogs = () => {
    const logText = filteredLogs
      .map(
        (log) =>
          `${log.timestamp} [${log.level}] ${log.logger} - ${log.message} (${log.module}:${log.function}:${log.line})`
      )
      .join('\n')

    const blob = new Blob([logText], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `logs-${new Date().toISOString()}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  if (!isExpanded) {
    return (
      <div className="fixed bottom-0 left-0 right-0 z-40 border-t bg-background">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setIsExpanded(true)}
          className="w-full justify-between px-4 py-2 rounded-none hover:bg-accent"
        >
          <div className="flex items-center gap-2">
            <Terminal className="w-4 h-4" />
            <span className="text-sm font-medium">Live Logs</span>
            <Badge variant={isConnected ? 'default' : 'destructive'} className="text-xs">
              {isConnected ? 'Connected' : 'Disconnected'}
            </Badge>
            <Badge variant="secondary" className="text-xs">
              {logs.length} entries
            </Badge>
          </div>
          <ChevronUp className="w-4 h-4" />
        </Button>
      </div>
    )
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 z-40 border-t bg-background shadow-lg">
      <Card className="rounded-none border-0 border-t">
        <CardHeader className="py-3 px-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Terminal className="w-5 h-5 text-primary" />
              <CardTitle className="text-base">Live Logs</CardTitle>
              <Badge variant={isConnected ? 'default' : 'destructive'} className="text-xs">
                {isConnected ? 'Connected' : 'Disconnected'}
              </Badge>
              <Badge variant="secondary" className="text-xs">
                {filteredLogs.length} / {logs.length}
              </Badge>
            </div>

            <div className="flex items-center gap-2">
              {/* Search */}
              <div className="relative w-64">
                <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Search logs..."
                  value={searchText}
                  onChange={(e) => setSearchText(e.target.value)}
                  className="pl-8 h-8 text-sm"
                />
              </div>

              {/* Level Filter */}
              <select
                value={levelFilter}
                onChange={(e) => setLevelFilter(e.target.value)}
                className="h-8 text-sm border rounded px-2 bg-background"
              >
                <option value="all">All Levels</option>
                <option value="DEBUG">DEBUG</option>
                <option value="INFO">INFO</option>
                <option value="WARNING">WARNING</option>
                <option value="ERROR">ERROR</option>
                <option value="CRITICAL">CRITICAL</option>
              </select>

              {/* Step Filter */}
              <select
                value={stepFilter}
                onChange={(e) =>
                  setStepFilter(e.target.value === 'all' ? 'all' : parseInt(e.target.value))
                }
                className="h-8 text-sm border rounded px-2 bg-background"
              >
                <option value="all">All Steps</option>
                <option value="1">Step 1</option>
                <option value="2">Step 2</option>
                <option value="3">Step 3</option>
                <option value="4">Step 4</option>
                <option value="5">Step 5</option>
                <option value="6">Step 6</option>
              </select>

              {/* Actions */}
              <Button variant="outline" size="sm" onClick={handleDownloadLogs}>
                <Download className="w-4 h-4" />
              </Button>
              <Button variant="outline" size="sm" onClick={handleClearLogs}>
                <Trash2 className="w-4 h-4" />
              </Button>
              <Button variant="ghost" size="sm" onClick={() => setIsExpanded(false)}>
                <ChevronDown className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </CardHeader>

        <CardContent className="p-0">
          <ScrollArea
            ref={scrollRef}
            className="font-mono text-xs"
            style={{ height: maxHeight }}
          >
            <div className="p-4 space-y-1">
              {error && (
                <div className="text-red-500 bg-red-50 dark:bg-red-950 p-2 rounded">
                  ⚠️ {error}
                </div>
              )}

              {filteredLogs.length === 0 && (
                <div className="text-muted-foreground text-center py-8">
                  No logs to display
                  {searchText && ' (try adjusting filters)'}
                </div>
              )}

              {filteredLogs.map((log, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-2 p-1 hover:bg-accent/50 rounded"
                >
                  <span className="text-muted-foreground shrink-0">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <Badge
                    variant="outline"
                    className={`shrink-0 text-xs ${LEVEL_COLORS[log.level]}`}
                  >
                    {log.level}
                  </Badge>
                  {log.step && (
                    <Badge variant="secondary" className="shrink-0 text-xs">
                      S{log.step}
                    </Badge>
                  )}
                  <span className="text-muted-foreground shrink-0">{log.module}</span>
                  <span className="flex-1 break-all">{log.message}</span>
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  )
}
