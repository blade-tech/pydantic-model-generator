'use client'

/**
 * Step 3: OutcomeSpec Generation
 *
 * Generate OutcomeSpec YAML with:
 * - Outcome questions
 * - Target entities
 * - Validation queries (Cypher)
 *
 * Features:
 * - Real-time streaming of Claude's generation
 * - YAML syntax highlighting
 * - Human approval gate
 */

import { useState } from 'react'
import { useWorkflowStore } from '@/lib/workflow-store'
import { generateOutcomeSpec } from '@/lib/api-client'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { Textarea } from '@/components/ui/textarea'
import { ArrowLeft, ArrowRight, Loader2, FileText, CheckCircle } from 'lucide-react'
import { PromptEditor } from './PromptEditor'

export default function Step3OutcomeSpec() {
  const {
    businessText,
    entities,
    outcomeSpec,
    setCurrentStep,
    setOutcomeSpec,
    approveOutcomeSpec,
    setLoading,
    error,
    setError,
    setStreamingContent,
    appendStreamingContent,
    streamingContent
  } = useWorkflowStore()

  const [hasStarted, setHasStarted] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const [isComplete, setIsComplete] = useState(false)
  const [localSpec, setLocalSpec] = useState(outcomeSpec)
  const [customPrompt, setCustomPrompt] = useState<string | null>(null)

  const startGeneration = async () => {
    setHasStarted(true)
    setIsStreaming(true)
    setLoading(true)
    setError(null)
    setStreamingContent('')

    try {
      const stream = generateOutcomeSpec(businessText, entities, customPrompt || undefined)

      for await (const event of stream) {
        if (event.type === 'chunk') {
          appendStreamingContent(event.content)
        } else if (event.type === 'complete') {
          setOutcomeSpec(event.result.yaml_content)
          setLocalSpec(event.result.yaml_content)
          setIsComplete(true)
          setIsStreaming(false)
          setLoading(false)
        } else if (event.type === 'error') {
          setError(event.error.detail)
          setIsStreaming(false)
          setLoading(false)
        }
      }
    } catch (error: any) {
      setError(error.message)
      setIsStreaming(false)
      setLoading(false)
    }
  }

  const handleApprove = () => {
    setOutcomeSpec(localSpec)
    approveOutcomeSpec()
  }

  const handleBack = () => {
    setCurrentStep(2)
  }

  const canApprove = isComplete && localSpec.trim().length > 0

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Step 3: OutcomeSpec Generation
          </CardTitle>
          <CardDescription>
            Generate an OutcomeSpec YAML with outcome questions and validation queries.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {!hasStarted && (
            <div className="space-y-4">
              <div className="text-center">
                <p className="text-sm text-muted-foreground mb-4">
                  Ready to generate OutcomeSpec from identified entities.
                </p>
              </div>

              <PromptEditor
                stepId="step3_outcome_spec"
                onPromptChange={setCustomPrompt}
                currentCustomPrompt={customPrompt}
              />

              <div className="text-center">
                <Button onClick={startGeneration} size="lg">
                  <FileText className="w-4 h-4 mr-2" />
                  Generate OutcomeSpec
                </Button>
              </div>
            </div>
          )}

          {hasStarted && (
            <>
              {/* Claude Thinking Log */}
              <Accordion type="single" collapsible defaultValue="thinking">
                <AccordionItem value="thinking">
                  <AccordionTrigger>
                    <div className="flex items-center gap-2">
                      {isStreaming && <Loader2 className="w-4 h-4 animate-spin" />}
                      {isComplete && <CheckCircle className="w-4 h-4 text-green-500" />}
                      <span>Claude Generation Log</span>
                      <Badge variant={isStreaming ? "default" : "secondary"}>
                        {isStreaming ? "Generating..." : "Complete"}
                      </Badge>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent>
                    <div className="bg-muted rounded-lg p-4 max-h-96 overflow-y-auto">
                      <pre className="text-xs font-mono whitespace-pre-wrap">
                        {streamingContent || "Waiting for Claude..."}
                      </pre>
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>

              {/* Error Display */}
              {!isStreaming && error && (
                <Card className="border-red-500">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-2">
                      <FileText className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                      <div>
                        <h4 className="text-sm font-medium text-red-600 mb-1">Error During Generation</h4>
                        <p className="text-xs text-red-600">{error}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Generated OutcomeSpec YAML */}
              {isComplete && (
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="text-sm font-medium">
                      Generated OutcomeSpec (editable)
                    </h3>
                    <Badge variant="secondary">YAML</Badge>
                  </div>
                  <Textarea
                    value={localSpec}
                    onChange={(e) => setLocalSpec(e.target.value)}
                    rows={20}
                    className="font-mono text-xs"
                    placeholder="OutcomeSpec YAML will appear here..."
                  />
                  <p className="text-xs text-muted-foreground mt-2">
                    You can edit the YAML before approving. Changes will be saved.
                  </p>
                </div>
              )}
            </>
          )}

          {/* Actions */}
          <div className="flex justify-between items-center pt-4">
            <Button variant="outline" onClick={handleBack}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <Button
              onClick={handleApprove}
              disabled={!canApprove}
              size="lg"
            >
              Approve & Continue
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Info */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">What is OutcomeSpec?</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-xs text-muted-foreground mb-2">
            OutcomeSpec is a YAML specification that defines:
          </p>
          <ul className="text-xs text-muted-foreground space-y-1 list-disc list-inside">
            <li><strong>Outcome Questions:</strong> What questions does this schema answer?</li>
            <li><strong>Target Entities:</strong> Which entities are involved?</li>
            <li><strong>Validation Queries:</strong> Cypher queries to validate data integrity</li>
            <li><strong>Business Context:</strong> Why these entities matter for your use case</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}
