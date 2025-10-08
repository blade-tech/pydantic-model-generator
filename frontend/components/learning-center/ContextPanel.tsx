'use client'

/**
 * Context Panel - Learning Center Component
 *
 * Displays contextual help, file references, libraries, and tips
 * for the current workflow step. Can be collapsed/expanded.
 */

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { ScrollArea } from '@/components/ui/scroll-area'
import {
  ChevronLeft,
  ChevronRight,
  BookOpen,
  FileCode,
  Package,
  Lightbulb,
  AlertCircle
} from 'lucide-react'

interface StepHelp {
  step_number: number
  step_name: string
  description: string
  files_used: string[]
  libraries: string[]
  tips: string[]
}

interface ContextPanelProps {
  currentStep: number
  onFileClick?: (filePath: string) => void
}

export default function ContextPanel({ currentStep, onFileClick }: ContextPanelProps) {
  const [isExpanded, setIsExpanded] = useState(true)
  const [helpContent, setHelpContent] = useState<StepHelp | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Fetch help content for current step
  useEffect(() => {
    const fetchHelpContent = async () => {
      setIsLoading(true)
      setError(null)

      try {
        const response = await fetch(
          `http://localhost:8000/api/learning-center/help/step/${currentStep}`
        )

        if (!response.ok) {
          throw new Error(`Failed to fetch help content: ${response.statusText}`)
        }

        const data = await response.json()
        setHelpContent(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load help content')
        console.error('Error fetching help content:', err)
      } finally {
        setIsLoading(false)
      }
    }

    if (currentStep >= 1 && currentStep <= 6) {
      fetchHelpContent()
    }
  }, [currentStep])

  if (!isExpanded) {
    return (
      <div className="fixed right-0 top-20 z-40">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsExpanded(true)}
          className="rounded-l-md rounded-r-none shadow-lg"
        >
          <ChevronLeft className="w-4 h-4" />
          <BookOpen className="w-4 h-4 ml-1" />
        </Button>
      </div>
    )
  }

  return (
    <div className="fixed right-0 top-20 bottom-0 w-96 bg-background border-l shadow-lg z-40 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-primary" />
          <h2 className="font-semibold text-lg">Context Panel</h2>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setIsExpanded(false)}
        >
          <ChevronRight className="w-4 h-4" />
        </Button>
      </div>

      {/* Content */}
      <ScrollArea className="flex-1">
        <div className="p-4 space-y-6">
          {isLoading && (
            <div className="text-center py-8 text-muted-foreground">
              Loading help content...
            </div>
          )}

          {error && (
            <Card className="border-destructive">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-destructive">
                  <AlertCircle className="w-5 h-5" />
                  Error
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm">{error}</p>
              </CardContent>
            </Card>
          )}

          {helpContent && (
            <>
              {/* Step Info */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Badge variant="default" className="text-xs">
                      Step {helpContent.step_number}
                    </Badge>
                  </div>
                  <CardTitle className="text-lg">{helpContent.step_name}</CardTitle>
                  <CardDescription className="text-sm leading-relaxed">
                    {helpContent.description}
                  </CardDescription>
                </CardHeader>
              </Card>

              {/* Files Used */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-sm">
                    <FileCode className="w-4 h-4" />
                    Files Being Used
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {helpContent.files_used.map((file, idx) => (
                      <button
                        key={idx}
                        onClick={() => onFileClick?.(file)}
                        className="text-xs font-mono text-left w-full p-2 rounded hover:bg-accent transition-colors text-primary hover:underline"
                      >
                        {file}
                      </button>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Libraries */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-sm">
                    <Package className="w-4 h-4" />
                    Libraries & Technologies
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {helpContent.libraries.map((lib, idx) => (
                      <Badge key={idx} variant="secondary" className="text-xs">
                        {lib}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Tips */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-sm">
                    <Lightbulb className="w-4 h-4" />
                    Tips & Best Practices
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {helpContent.tips.map((tip, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <span className="text-primary mt-1">•</span>
                        <span className="flex-1">{tip}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </>
          )}
        </div>
      </ScrollArea>

      {/* Footer */}
      <div className="p-4 border-t">
        <p className="text-xs text-muted-foreground text-center">
          Context help for Step {currentStep}
        </p>
      </div>
    </div>
  )
}
