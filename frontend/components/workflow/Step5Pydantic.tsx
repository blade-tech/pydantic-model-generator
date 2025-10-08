'use client'

/**
 * Step 5: Pydantic Model Generation
 *
 * Execute gen-pydantic subprocess to generate Pydantic V2 models.
 * Writes files to pydantic_library/generated/pydantic/overlays/
 *
 * Features:
 * - Display subprocess output
 * - Show generated Python code
 * - Highlight validation errors
 * - Human approval gate
 */

import { useState } from 'react'
import { useWorkflowStore } from '@/lib/workflow-store'
import { generatePydanticModels } from '@/lib/api-client'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { ArrowLeft, ArrowRight, Loader2, Code, CheckCircle, AlertCircle } from 'lucide-react'

export default function Step5Pydantic() {
  const {
    linkmlSchema,
    overlayName,
    pythonCode,
    generationSuccess,
    setCurrentStep,
    setPythonCode,
    setGenerationSuccess,
    setLoading,
    setError
  } = useWorkflowStore()

  const [hasStarted, setHasStarted] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [outputPath, setOutputPath] = useState('')
  const [stderr, setStderr] = useState('')

  const startGeneration = async () => {
    setHasStarted(true)
    setIsGenerating(true)
    setLoading(true)
    setError(null)

    try {
      const result = await generatePydanticModels(overlayName, linkmlSchema)

      setPythonCode(result.python_code)
      setGenerationSuccess(result.success)
      setOutputPath(result.output_path)
      setStderr(result.stderr || '')
      setIsGenerating(false)
      setLoading(false)

      if (!result.success) {
        setError('Pydantic generation failed. Check error output below.')
      }
    } catch (error: any) {
      setError(error.message)
      setGenerationSuccess(false)
      setIsGenerating(false)
      setLoading(false)
    }
  }

  const handleApprove = () => {
    setCurrentStep(6)
  }

  const handleBack = () => {
    setCurrentStep(4)
  }

  const canApprove = hasStarted && generationSuccess && pythonCode.length > 0

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Code className="w-5 h-5" />
            Step 5: Pydantic Model Generation
          </CardTitle>
          <CardDescription>
            Execute gen-pydantic subprocess to generate Pydantic V2 models from LinkML schema.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {!hasStarted && (
            <div className="text-center py-8">
              <p className="text-sm text-muted-foreground mb-4">
                Ready to generate Pydantic V2 models using gen-pydantic subprocess.
              </p>
              <Button onClick={startGeneration} size="lg">
                <Code className="w-4 h-4 mr-2" />
                Generate Pydantic Models
              </Button>
            </div>
          )}

          {hasStarted && (
            <>
              {/* Generation Status */}
              <div className="flex items-center gap-2">
                {isGenerating && (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm">Running gen-pydantic subprocess...</span>
                  </>
                )}
                {!isGenerating && generationSuccess && (
                  <>
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span className="text-sm text-green-600">Generation successful!</span>
                  </>
                )}
                {!isGenerating && !generationSuccess && (
                  <>
                    <AlertCircle className="w-4 h-4 text-red-500" />
                    <span className="text-sm text-red-600">Generation failed</span>
                  </>
                )}
              </div>

              {/* Output Path */}
              {outputPath && (
                <div className="bg-muted rounded-lg p-3">
                  <p className="text-xs text-muted-foreground mb-1">Output file:</p>
                  <code className="text-xs font-mono">{outputPath}</code>
                </div>
              )}

              {/* Error Output (if any) */}
              {stderr && (
                <Accordion type="single" collapsible>
                  <AccordionItem value="stderr">
                    <AccordionTrigger>
                      <div className="flex items-center gap-2">
                        <AlertCircle className="w-4 h-4 text-yellow-500" />
                        <span>Subprocess Errors</span>
                        <Badge variant="destructive">stderr</Badge>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent>
                      <div className="bg-red-50 dark:bg-red-950 rounded-lg p-4 max-h-96 overflow-y-auto">
                        <pre className="text-xs font-mono whitespace-pre-wrap text-red-600 dark:text-red-400">
                          {stderr}
                        </pre>
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              )}

              {/* Generated Python Code */}
              {pythonCode && (
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="text-sm font-medium">Generated Pydantic Code</h3>
                    <Badge variant="secondary">Python</Badge>
                  </div>
                  <div className="bg-muted rounded-lg p-4 max-h-[600px] overflow-y-auto">
                    <pre className="text-xs font-mono whitespace-pre-wrap">
                      {pythonCode}
                    </pre>
                  </div>
                  <p className="text-xs text-muted-foreground mt-2">
                    File written to: ../pydantic_library/generated/pydantic/overlays/{overlayName}_models.py
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
              Continue to Testing
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Info */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">What Happens Here?</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="text-xs text-muted-foreground space-y-1 list-decimal list-inside">
            <li>LinkML schema is written to ../pydantic_library/schemas/overlays/</li>
            <li>gen-pydantic subprocess is executed via subprocess.run()</li>
            <li>Pydantic V2 models are generated with validation</li>
            <li>Output is written to ../pydantic_library/generated/pydantic/overlays/</li>
            <li>Stdout contains generated Python code</li>
            <li>Stderr contains any errors or warnings</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}
