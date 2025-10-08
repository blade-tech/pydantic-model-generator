'use client'

/**
 * Step 2: AI Ontology Research
 *
 * Claude analyzes business text and identifies 2-8 key entities,
 * mapping them to canonical ontology URIs with confidence scores.
 *
 * Features:
 * - Human-in-the-loop: Add context and instructions before research
 * - Optional MCP tool usage (web search, etc.)
 * - Real-time streaming of Claude's reasoning
 * - Entity mapping table with confidence scores
 * - Human approval gate
 */

import { useState, useEffect } from 'react'
import { useWorkflowStore } from '@/lib/workflow-store'
import { researchOntologies } from '@/lib/api-client'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { Separator } from '@/components/ui/separator'
import { ArrowLeft, ArrowRight, Loader2, Brain, CheckCircle, ExternalLink, MessageSquarePlus } from 'lucide-react'
import { PromptEditor } from './PromptEditor'

export default function Step2OntologyResearch() {
  const {
    businessText,
    entities,
    reasoningLog,
    setCurrentStep,
    setEntities,
    setReasoningLog,
    appendReasoningLog,
    approveResearch,
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

  // New: User context and instructions
  const [userContext, setUserContext] = useState('')
  const [useMcpTools, setUseMcpTools] = useState(false)
  const [customPrompt, setCustomPrompt] = useState<string | null>(null)

  const startResearch = async () => {
    setHasStarted(true)
    setIsStreaming(true)
    setIsComplete(false)  // Reset completion state for re-runs
    setLoading(true)
    setError(null)
    setStreamingContent('')
    setReasoningLog([])
    setEntities([])  // Clear previous entities for re-runs

    try {
      // Pass user context and custom prompt to API
      const stream = researchOntologies(businessText, userContext, useMcpTools, customPrompt || undefined)

      for await (const event of stream) {
        if (event.type === 'chunk') {
          appendStreamingContent(event.content)
          appendReasoningLog(event.content)
        } else if (event.type === 'complete') {
          setEntities(event.result.entities)
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
    approveResearch()
  }

  const handleBack = () => {
    setCurrentStep(1)
  }

  const canApprove = isComplete && entities.length > 0

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5" />
            Step 2: AI Ontology Research
          </CardTitle>
          <CardDescription>
            Claude analyzes your business text to identify key entities and map them to canonical ontologies.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {!hasStarted && (
            <div className="space-y-4">
              <div>
                <h3 className="text-sm font-medium mb-2 flex items-center gap-2">
                  <MessageSquarePlus className="w-4 h-4" />
                  Add Context or Instructions (Optional)
                </h3>
                <p className="text-xs text-muted-foreground mb-3">
                  Guide Claude's research by adding specific requirements, domain knowledge, or constraints.
                </p>
                <Textarea
                  value={userContext}
                  onChange={(e) => setUserContext(e.target.value)}
                  placeholder="Example: Focus on financial compliance entities. Use Islamic banking terminology. Check if any entities relate to Murabaha contracts..."
                  rows={6}
                  className="text-sm"
                />
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="mcp-tools"
                  checked={useMcpTools}
                  onCheckedChange={(checked) => setUseMcpTools(checked as boolean)}
                />
                <Label htmlFor="mcp-tools" className="text-sm font-normal cursor-pointer">
                  Enable MCP Tools (web search, documentation lookup)
                </Label>
              </div>

              <PromptEditor
                stepId="step2_research"
                onPromptChange={setCustomPrompt}
                currentCustomPrompt={customPrompt}
              />

              <Separator />

              <div className="flex justify-center">
                <Button onClick={startResearch} size="lg">
                  <Brain className="w-4 h-4 mr-2" />
                  Start Research
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
                      <span>Claude Thinking Log</span>
                      <Badge variant={isStreaming ? "default" : "secondary"}>
                        {isStreaming ? "Streaming..." : "Complete"}
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
                      <ExternalLink className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                      <div>
                        <h4 className="text-sm font-medium text-red-600 mb-1">Error During Research</h4>
                        <p className="text-xs text-red-600">{error}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Entity Mappings */}
              {isComplete && entities.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium mb-3">
                    Identified Entities ({entities.length})
                  </h3>
                  <div className="space-y-2">
                    {entities.map((entity, index) => (
                      <Card key={index}>
                        <CardContent className="p-4">
                          <div className="flex justify-between items-start mb-2">
                            <div>
                              <h4 className="font-medium">{entity.entity_name}</h4>
                              <Badge variant="outline" className="text-xs mt-1">
                                {entity.entity_type}
                              </Badge>
                            </div>
                            <div className="text-right">
                              <Badge
                                variant={entity.confidence >= 0.8 ? "default" : entity.confidence >= 0.6 ? "secondary" : "outline"}
                              >
                                {(entity.confidence * 100).toFixed(0)}% confidence
                              </Badge>
                            </div>
                          </div>
                          <Separator className="my-2" />
                          <div className="space-y-2">
                            <div className="flex items-center gap-2 text-xs">
                              <Badge variant="outline">{entity.ontology_source}</Badge>
                              <a
                                href={entity.ontology_uri}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-500 hover:underline flex items-center gap-1"
                              >
                                {entity.ontology_uri}
                                <ExternalLink className="w-3 h-3" />
                              </a>
                            </div>
                            <p className="text-xs text-muted-foreground">
                              {entity.reasoning}
                            </p>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              )}

              {/* Refine & Re-run Section */}
              {isComplete && (
                <div className="mt-6">
                  <Separator className="my-4" />
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-sm font-medium mb-2 flex items-center gap-2">
                        <MessageSquarePlus className="w-4 h-4" />
                        Refine Context & Re-run (Optional)
                      </h3>
                      <p className="text-xs text-muted-foreground mb-3">
                        Not satisfied with the results? Add more context or change your instructions and re-run the research.
                      </p>
                      <Textarea
                        value={userContext}
                        onChange={(e) => setUserContext(e.target.value)}
                        placeholder="Add additional context or modify existing instructions..."
                        rows={4}
                        className="text-sm"
                      />
                    </div>

                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="mcp-tools-rerun"
                        checked={useMcpTools}
                        onCheckedChange={(checked) => setUseMcpTools(checked as boolean)}
                      />
                      <Label htmlFor="mcp-tools-rerun" className="text-sm font-normal cursor-pointer">
                        Enable MCP Tools (web search, documentation lookup)
                      </Label>
                    </div>

                    <div className="flex justify-center">
                      <Button onClick={startResearch} variant="outline" size="sm">
                        <Brain className="w-4 h-4 mr-2" />
                        Re-run Research
                      </Button>
                    </div>
                  </div>
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
          <CardTitle className="text-sm">Ontology Sources</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="text-xs text-muted-foreground space-y-1">
            <li><strong>DoCO:</strong> Document Components Ontology</li>
            <li><strong>FaBiO:</strong> FRBR-aligned Bibliographic Ontology</li>
            <li><strong>PROV-O:</strong> Provenance Ontology</li>
            <li><strong>FIBO:</strong> Financial Industry Business Ontology</li>
            <li><strong>SKOS:</strong> Simple Knowledge Organization System</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}
