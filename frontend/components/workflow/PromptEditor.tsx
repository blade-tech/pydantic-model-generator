"use client"

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Code2, RotateCcw, AlertCircle, Info } from 'lucide-react'
import { getDefaultPrompt } from '@/lib/api-client'

interface PromptEditorProps {
  stepId: string  // e.g., 'step2_research', 'step3_outcome_spec', 'step4_linkml'
  onPromptChange: (customPrompt: string | null) => void
  currentCustomPrompt?: string | null
}

export function PromptEditor({ stepId, onPromptChange, currentCustomPrompt }: PromptEditorProps) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [promptData, setPromptData] = useState<any>(null)
  const [isEditing, setIsEditing] = useState(false)
  const [customPromptText, setCustomPromptText] = useState('')

  // Load default prompt on mount
  useEffect(() => {
    loadDefaultPrompt()
  }, [stepId])

  // Initialize custom prompt if provided
  useEffect(() => {
    if (currentCustomPrompt) {
      setCustomPromptText(currentCustomPrompt)
      setIsEditing(true)
    }
  }, [currentCustomPrompt])

  const loadDefaultPrompt = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getDefaultPrompt(stepId)
      setPromptData(data)
    } catch (err: any) {
      setError(err.message || 'Failed to load prompt')
    } finally {
      setLoading(false)
    }
  }

  const handleResetToDefault = () => {
    setCustomPromptText('')
    setIsEditing(false)
    onPromptChange(null)
  }

  const handleUseCustomPrompt = () => {
    if (customPromptText.trim()) {
      onPromptChange(customPromptText)
    } else {
      onPromptChange(null)
    }
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Code2 className="w-5 h-5" />
            Loading Prompt...
          </CardTitle>
        </CardHeader>
      </Card>
    )
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="w-4 h-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    )
  }

  if (!promptData) {
    return null
  }

  return (
    <Accordion type="single" collapsible className="w-full">
      <AccordionItem value="prompt-editor">
        <AccordionTrigger className="text-sm font-medium">
          <div className="flex items-center gap-2">
            <Code2 className="w-4 h-4" />
            <span>View/Edit AI Prompt (Advanced)</span>
            {customPromptText && (
              <Badge variant="secondary" className="ml-2">Custom</Badge>
            )}
          </div>
        </AccordionTrigger>
        <AccordionContent>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">{promptData.step}</CardTitle>
              <CardDescription>{promptData.description}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Variables Info */}
              {promptData.variables && promptData.variables.length > 0 && (
                <Alert>
                  <Info className="w-4 h-4" />
                  <AlertDescription>
                    <div className="font-medium mb-2">Available Variables:</div>
                    <ul className="space-y-1 text-xs">
                      {promptData.variables.map((v: any) => (
                        <li key={v.name}>
                          <code className="bg-muted px-1 py-0.5 rounded">{`{${v.name}}`}</code> - {v.description}
                        </li>
                      ))}
                    </ul>
                  </AlertDescription>
                </Alert>
              )}

              {/* Default Prompt Display */}
              {!isEditing && (
                <div className="space-y-3">
                  <div>
                    <div className="text-sm font-medium mb-2">System Prompt:</div>
                    <ScrollArea className="h-[100px] rounded-md border p-3 bg-muted/30">
                      <pre className="text-xs whitespace-pre-wrap font-mono">{promptData.system}</pre>
                    </ScrollArea>
                  </div>

                  <div>
                    <div className="text-sm font-medium mb-2">Task Prompt:</div>
                    <ScrollArea className="h-[200px] rounded-md border p-3 bg-muted/30">
                      <pre className="text-xs whitespace-pre-wrap font-mono">{promptData.task}</pre>
                    </ScrollArea>
                  </div>

                  <Button
                    onClick={() => setIsEditing(true)}
                    variant="outline"
                    size="sm"
                    className="w-full"
                  >
                    <Code2 className="w-4 h-4 mr-2" />
                    Edit Custom Prompt
                  </Button>
                </div>
              )}

              {/* Custom Prompt Editor */}
              {isEditing && (
                <div className="space-y-3">
                  <Alert>
                    <AlertCircle className="w-4 h-4" />
                    <AlertDescription>
                      Write your custom prompt below. Use the variable placeholders shown above to insert dynamic values.
                      Leave empty and click "Reset to Default" to use the default prompt.
                    </AlertDescription>
                  </Alert>

                  <div>
                    <div className="text-sm font-medium mb-2">Custom Prompt:</div>
                    <Textarea
                      value={customPromptText}
                      onChange={(e) => setCustomPromptText(e.target.value)}
                      placeholder="Write your custom prompt here, or leave empty to use default..."
                      rows={15}
                      className="font-mono text-xs"
                    />
                  </div>

                  <div className="flex gap-2">
                    <Button
                      onClick={handleUseCustomPrompt}
                      size="sm"
                      className="flex-1"
                    >
                      Use Custom Prompt
                    </Button>
                    <Button
                      onClick={handleResetToDefault}
                      variant="outline"
                      size="sm"
                      className="flex-1"
                    >
                      <RotateCcw className="w-4 h-4 mr-2" />
                      Reset to Default
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  )
}
