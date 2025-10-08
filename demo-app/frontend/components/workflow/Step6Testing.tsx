'use client'

/**
 * Step 6: Testing & Ingestion
 *
 * Run pytest on generated models and optionally ingest to Graphiti/Neo4j.
 *
 * Features:
 * - Display pytest results
 * - Show pass/fail/skip counts
 * - Display test details
 * - Reset workflow for new run
 */

import { useState } from 'react'
import { useWorkflowStore } from '@/lib/workflow-store'
import { runTests } from '@/lib/api-client'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { ArrowLeft, Loader2, CheckCircle, XCircle, MinusCircle, RefreshCw, PlayCircle } from 'lucide-react'

export default function Step6Testing() {
  const {
    overlayName,
    testResults,
    setCurrentStep,
    setTestResults,
    setLoading,
    setError,
    resetWorkflow
  } = useWorkflowStore()

  const [hasStarted, setHasStarted] = useState(false)
  const [isTesting, setIsTesting] = useState(false)

  const startTesting = async () => {
    setHasStarted(true)
    setIsTesting(true)
    setLoading(true)
    setError(null)

    try {
      const result = await runTests(overlayName)
      setTestResults(result)
      setIsTesting(false)
      setLoading(false)

      if (!result.success) {
        setError('Some tests failed. Check test details below.')
      }
    } catch (error: any) {
      setError(error.message)
      setIsTesting(false)
      setLoading(false)
    }
  }

  const handleBack = () => {
    setCurrentStep(5)
  }

  const handleReset = () => {
    if (confirm('Reset workflow? This will clear all current data.')) {
      resetWorkflow()
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <PlayCircle className="w-5 h-5" />
            Step 6: Testing & Results
          </CardTitle>
          <CardDescription>
            Run pytest on generated Pydantic models to validate schema compliance.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {!hasStarted && (
            <div className="text-center py-8">
              <p className="text-sm text-muted-foreground mb-4">
                Ready to run pytest on generated models.
              </p>
              <Button onClick={startTesting} size="lg">
                <PlayCircle className="w-4 h-4 mr-2" />
                Run Tests
              </Button>
            </div>
          )}

          {hasStarted && (
            <>
              {/* Test Status */}
              <div className="flex items-center gap-2">
                {isTesting && (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm">Running pytest...</span>
                  </>
                )}
                {!isTesting && testResults && (
                  <>
                    {testResults.success ? (
                      <>
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span className="text-sm text-green-600">All tests passed!</span>
                      </>
                    ) : (
                      <>
                        <XCircle className="w-4 h-4 text-red-500" />
                        <span className="text-sm text-red-600">Some tests failed</span>
                      </>
                    )}
                  </>
                )}
              </div>

              {/* Test Summary */}
              {testResults && (
                <div className="grid grid-cols-4 gap-4">
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold">{testResults.total_tests}</div>
                      <div className="text-xs text-muted-foreground">Total Tests</div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-green-500">{testResults.passed}</div>
                      <div className="text-xs text-muted-foreground">Passed</div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-red-500">{testResults.failed}</div>
                      <div className="text-xs text-muted-foreground">Failed</div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-yellow-500">{testResults.skipped}</div>
                      <div className="text-xs text-muted-foreground">Skipped</div>
                    </CardContent>
                  </Card>
                </div>
              )}

              {/* Test Details */}
              {testResults && testResults.tests && testResults.tests.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium mb-3">Test Details</h3>
                  <div className="space-y-2">
                    {testResults.tests.map((test: any, index: number) => (
                      <Card key={index}>
                        <CardContent className="p-3">
                          <div className="flex items-start gap-3">
                            <div className="pt-1">
                              {test.passed && <CheckCircle className="w-4 h-4 text-green-500" />}
                              {test.failed && <XCircle className="w-4 h-4 text-red-500" />}
                              {test.skipped && <MinusCircle className="w-4 h-4 text-yellow-500" />}
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <code className="text-xs font-mono">{test.name}</code>
                                <Badge
                                  variant={test.passed ? "default" : test.failed ? "destructive" : "secondary"}
                                  className="text-xs"
                                >
                                  {test.passed ? "PASS" : test.failed ? "FAIL" : "SKIP"}
                                </Badge>
                              </div>
                              {test.duration && (
                                <p className="text-xs text-muted-foreground">
                                  Duration: {test.duration.toFixed(3)}s
                                </p>
                              )}
                              {test.message && (
                                <p className="text-xs text-red-600 mt-2">{test.message}</p>
                              )}
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              )}

              {/* Pytest Stderr - Error Output (SHOW FIRST IF EXISTS) */}
              {testResults && testResults.stderr && (
                <div>
                  <h3 className="text-sm font-medium mb-2 text-red-600">Error Output (stderr)</h3>
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4 max-h-96 overflow-y-auto">
                    <pre className="text-xs font-mono whitespace-pre-wrap text-red-800">
                      {testResults.stderr}
                    </pre>
                  </div>
                </div>
              )}

              {/* Pytest Stdout */}
              {testResults && testResults.stdout && (
                <div>
                  <h3 className="text-sm font-medium mb-2">Test Output (stdout)</h3>
                  <div className="bg-muted rounded-lg p-4 max-h-96 overflow-y-auto">
                    <pre className="text-xs font-mono whitespace-pre-wrap">
                      {testResults.stdout}
                    </pre>
                  </div>
                </div>
              )}
            </>
          )}

          <Separator className="my-4" />

          {/* Actions */}
          <div className="flex justify-between items-center">
            <Button variant="outline" onClick={handleBack}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <div className="flex gap-2">
              {testResults && (
                <Button variant="outline" onClick={handleReset}>
                  <RefreshCw className="w-4 h-4 mr-2" />
                  New Workflow
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Success Message */}
      {testResults && testResults.success && (
        <Card className="border-green-500">
          <CardHeader>
            <CardTitle className="text-green-500 flex items-center gap-2">
              <CheckCircle className="w-5 h-5" />
              Pipeline Complete!
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Your Pydantic models have been successfully generated and validated.
            </p>
            <div className="space-y-2 text-xs text-muted-foreground">
              <p><strong>Files Created:</strong></p>
              <ul className="list-disc list-inside space-y-1">
                <li>LinkML Schema: ../pydantic_library/schemas/overlays/{overlayName}_overlay.yaml</li>
                <li>Pydantic Models: ../pydantic_library/generated/pydantic/overlays/{overlayName}_models.py</li>
              </ul>
              <p className="mt-4">
                <strong>Next Steps:</strong>
              </p>
              <ul className="list-disc list-inside space-y-1">
                <li>Import generated models in your Python code</li>
                <li>Use models for data validation and serialization</li>
                <li>Integrate with Graphiti for knowledge graph ingestion (optional)</li>
                <li>Add custom tests in pydantic_library/tests/</li>
              </ul>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Info */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Testing Details</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="text-xs text-muted-foreground space-y-1 list-disc list-inside">
            <li>Tests run in pydantic_library context using pytest</li>
            <li>Validates Pydantic model structure and constraints</li>
            <li>Checks serialization/deserialization (model_dump, model_validate)</li>
            <li>Verifies field types and validation rules</li>
            <li>Test files located in: ../pydantic_library/tests/</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}
