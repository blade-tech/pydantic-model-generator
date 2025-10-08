'use client'

/**
 * Step 4: LinkML Schema Generation
 *
 * Generate LinkML schema YAML with:
 * - Class definitions
 * - Canonical ontology URIs (class_uri)
 * - ProvenanceFields mixin
 * - Slots (fields)
 * - Relationships
 *
 * Features:
 * - Real-time streaming of Claude's generation
 * - YAML syntax highlighting
 * - Entity count display
 * - Human approval gate
 */

import { useState } from 'react'
import { useWorkflowStore } from '@/lib/workflow-store'
import { generateLinkmlSchema } from '@/lib/api-client'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { Textarea } from '@/components/ui/textarea'
import { Input } from '@/components/ui/input'
import { ArrowLeft, ArrowRight, Loader2, Database, CheckCircle } from 'lucide-react'
import { PromptEditor } from './PromptEditor'

export default function Step4LinkML() {
  const {
    outcomeSpec,
    entities,
    linkmlSchema,
    overlayName,
    setCurrentStep,
    setLinkmlSchema,
    setOverlayName,
    approveLinkml,
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
  const [localSchema, setLocalSchema] = useState(linkmlSchema)
  const [localOverlayName, setLocalOverlayName] = useState(overlayName || 'business_outcome')
  const [entityCount, setEntityCount] = useState(0)
  const [customPrompt, setCustomPrompt] = useState<string | null>(null)

  const startGeneration = async () => {
    setHasStarted(true)
    setIsStreaming(true)
    setLoading(true)
    setError(null)
    setStreamingContent('')

    try {
      const stream = generateLinkmlSchema(outcomeSpec, entities, customPrompt || undefined)

      for await (const event of stream) {
        if (event.type === 'chunk') {
          appendStreamingContent(event.content)
        } else if (event.type === 'complete') {
          setLinkmlSchema(event.result.yaml_content)
          setLocalSchema(event.result.yaml_content)
          setEntityCount(event.result.entity_count)
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
    setLinkmlSchema(localSchema)
    setOverlayName(localOverlayName)
    approveLinkml()
  }

  const handleBack = () => {
    setCurrentStep(3)
  }

  const canApprove = isComplete && localSchema.trim().length > 0 && localOverlayName.trim().length > 0

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="w-5 h-5" />
            Step 4: LinkML Schema Generation
          </CardTitle>
          <CardDescription>
            Generate LinkML schema with canonical ontology URIs and provenance tracking.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Overlay Name Input */}
          <div>
            <label htmlFor="overlay-name" className="text-sm font-medium block mb-2">
              Overlay Name
            </label>
            <Input
              id="overlay-name"
              value={localOverlayName}
              onChange={(e) => setLocalOverlayName(e.target.value)}
              placeholder="e.g., murabaha_audit, customer_support"
              className="font-mono"
              disabled={hasStarted}
            />
            <p className="text-xs text-muted-foreground mt-1">
              This will be used for file names: {localOverlayName}_overlay.yaml
            </p>
          </div>

          {!hasStarted && (
            <div className="space-y-4">
              <div className="text-center">
                <p className="text-sm text-muted-foreground mb-4">
                  Ready to generate LinkML schema from OutcomeSpec.
                </p>
              </div>

              <PromptEditor
                stepId="step4_linkml"
                onPromptChange={setCustomPrompt}
                currentCustomPrompt={customPrompt}
              />

              <div className="text-center">
                <Button
                  onClick={startGeneration}
                  size="lg"
                  disabled={!localOverlayName.trim()}
                >
                  <Database className="w-4 h-4 mr-2" />
                  Generate LinkML Schema
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
                      <Database className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                      <div>
                        <h4 className="text-sm font-medium text-red-600 mb-1">Error During Schema Generation</h4>
                        <p className="text-xs text-red-600">{error}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Generated LinkML Schema */}
              {isComplete && (
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="text-sm font-medium">
                      Generated LinkML Schema (editable)
                    </h3>
                    <div className="flex gap-2">
                      <Badge variant="secondary">YAML</Badge>
                      <Badge variant="outline">{entityCount} entities</Badge>
                    </div>
                  </div>
                  <Textarea
                    value={localSchema}
                    onChange={(e) => setLocalSchema(e.target.value)}
                    rows={20}
                    className="font-mono text-xs"
                    placeholder="LinkML schema YAML will appear here..."
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
          <CardTitle className="text-sm">LinkML Features</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="text-xs text-muted-foreground space-y-1 list-disc list-inside">
            <li><strong>class_uri:</strong> Canonical ontology URIs for semantic interoperability</li>
            <li><strong>ProvenanceFields:</strong> Automatic tracking of created_at, updated_at, source</li>
            <li><strong>Slots:</strong> Field definitions with types, constraints, and descriptions</li>
            <li><strong>Relationships:</strong> Links between entities via slots and ranges</li>
            <li><strong>Validation:</strong> Built-in constraints for data quality</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}
