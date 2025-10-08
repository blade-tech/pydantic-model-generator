'use client'

/**
 * Main workflow page with 6-step pipeline
 *
 * Steps:
 * 1. Business Outcome Input
 * 2. AI Ontology Research (streaming)
 * 3. OutcomeSpec Generation (streaming)
 * 4. LinkML Schema Generation (streaming)
 * 5. Pydantic Model Generation
 * 6. Testing & Ingestion
 */

import { useWorkflowStore } from '@/lib/workflow-store'
import { Progress } from '@/components/ui/progress'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { CheckCircle2, Circle, Loader2 } from 'lucide-react'

// Step components (to be implemented)
import Step1BusinessInput from '@/components/workflow/Step1BusinessInput'
import Step2OntologyResearch from '@/components/workflow/Step2OntologyResearch'
import Step3OutcomeSpec from '@/components/workflow/Step3OutcomeSpec'
import Step4LinkML from '@/components/workflow/Step4LinkML'
import Step5Pydantic from '@/components/workflow/Step5Pydantic'
import Step6Testing from '@/components/workflow/Step6Testing'

const STEPS = [
  { number: 1, title: 'Business Outcome', description: 'Enter your business text' },
  { number: 2, title: 'Ontology Research', description: 'AI maps entities to ontologies' },
  { number: 3, title: 'OutcomeSpec', description: 'Generate outcome specification' },
  { number: 4, title: 'LinkML Schema', description: 'Generate LinkML schema' },
  { number: 5, title: 'Pydantic Models', description: 'Generate Pydantic code' },
  { number: 6, title: 'Testing', description: 'Run tests and ingest to graph' },
]

export default function WorkflowPage() {
  const { currentStep, isLoading, error } = useWorkflowStore()

  // Calculate progress percentage
  const progressPercent = ((currentStep - 1) / 6) * 100

  return (
    <div className="container mx-auto py-8 px-4 max-w-7xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Pydantic Model Generator</h1>
        <p className="text-muted-foreground">
          Transform business outcomes into validated Pydantic models
        </p>
      </div>

      {/* Progress Bar */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Pipeline Progress</CardTitle>
          <CardDescription>
            Step {currentStep} of 6: {STEPS[currentStep - 1].title}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Progress value={progressPercent} className="mb-4" />

          {/* Step indicators */}
          <div className="flex justify-between items-center">
            {STEPS.map((step) => {
              const isComplete = step.number < currentStep
              const isCurrent = step.number === currentStep
              const isPending = step.number > currentStep

              return (
                <div key={step.number} className="flex flex-col items-center gap-2 flex-1">
                  <div className="flex items-center justify-center">
                    {isComplete && (
                      <CheckCircle2 className="w-6 h-6 text-green-500" />
                    )}
                    {isCurrent && (
                      isLoading ? (
                        <Loader2 className="w-6 h-6 text-blue-500 animate-spin" />
                      ) : (
                        <Circle className="w-6 h-6 text-blue-500 fill-blue-500" />
                      )
                    )}
                    {isPending && (
                      <Circle className="w-6 h-6 text-muted-foreground" />
                    )}
                  </div>
                  <div className="text-center">
                    <Badge
                      variant={isCurrent ? "default" : isComplete ? "secondary" : "outline"}
                      className="text-xs mb-1"
                    >
                      {step.number}
                    </Badge>
                    <p className="text-xs font-medium">{step.title}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Error Display */}
      {error && (
        <Card className="mb-6 border-red-500">
          <CardHeader>
            <CardTitle className="text-red-500">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-red-600">{error}</p>
          </CardContent>
        </Card>
      )}

      <Separator className="my-6" />

      {/* Current Step Content */}
      <div className="min-h-[600px]">
        {currentStep === 1 && <Step1BusinessInput />}
        {currentStep === 2 && <Step2OntologyResearch />}
        {currentStep === 3 && <Step3OutcomeSpec />}
        {currentStep === 4 && <Step4LinkML />}
        {currentStep === 5 && <Step5Pydantic />}
        {currentStep === 6 && <Step6Testing />}
      </div>
    </div>
  )
}
