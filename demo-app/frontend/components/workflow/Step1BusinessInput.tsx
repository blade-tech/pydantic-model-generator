'use client'

/**
 * Step 1: Business Outcome Input
 *
 * User enters business text describing their outcome/use case.
 * This text will be analyzed by Claude to identify entities.
 */

import { useState } from 'react'
import { useWorkflowStore } from '@/lib/workflow-store'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, Sparkles } from 'lucide-react'

const EXAMPLE_TEXT = `We need to audit Murabaha transactions for Shariah compliance.

Our auditors need to:
1. Verify that the bank owns the asset before selling to customer
2. Check that profit markup is disclosed and transparent
3. Ensure payment terms follow Shariah principles
4. Track audit trail for all compliance checks

We want to generate structured data models that can:
- Store transaction details (bank, customer, asset, pricing)
- Track ownership transfer checkpoints
- Record audit evidence and compliance status
- Query transactions by compliance status

The data should integrate with our Neo4j graph database for relationship analysis.`

export default function Step1BusinessInput() {
  const { businessText, setBusinessText, setCurrentStep } = useWorkflowStore()
  const [localText, setLocalText] = useState(businessText || EXAMPLE_TEXT)

  const handleContinue = () => {
    setBusinessText(localText)
    setCurrentStep(2)
  }

  const isValid = localText.trim().length > 50

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="w-5 h-5" />
            Step 1: Business Outcome Input
          </CardTitle>
          <CardDescription>
            Describe your business outcome or use case. The AI will analyze this to identify key entities.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label htmlFor="business-text" className="text-sm font-medium block mb-2">
              Business Outcome Text
            </label>
            <Textarea
              id="business-text"
              placeholder="Describe your business outcome, use case, or requirements..."
              value={localText}
              onChange={(e) => setLocalText(e.target.value)}
              rows={15}
              className="font-mono text-sm"
            />
            <p className="text-xs text-muted-foreground mt-2">
              {localText.length} characters (minimum 50 characters required)
            </p>
          </div>

          <div className="flex justify-between items-center">
            <div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setLocalText(EXAMPLE_TEXT)}
              >
                Load Example
              </Button>
            </div>
            <Button
              onClick={handleContinue}
              disabled={!isValid}
              size="lg"
            >
              Continue to Research
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <Badge className="w-fit">Step 2</Badge>
            <CardTitle className="text-sm">Ontology Research</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-xs text-muted-foreground">
              Claude will analyze your text to identify 2-8 key entities and map them to canonical ontologies (DoCO, FaBiO, PROV-O, FIBO, SKOS).
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <Badge className="w-fit">Step 3-4</Badge>
            <CardTitle className="text-sm">Schema Generation</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-xs text-muted-foreground">
              Generate OutcomeSpec and LinkML schemas with validation queries and entity definitions.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <Badge className="w-fit">Step 5-6</Badge>
            <CardTitle className="text-sm">Code & Testing</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-xs text-muted-foreground">
              Generate Pydantic V2 models, run validation tests, and ingest to knowledge graph.
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Requirements */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">What Makes Good Input?</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="text-xs text-muted-foreground space-y-2 list-disc list-inside">
            <li><strong>Business Context:</strong> Explain what you're trying to achieve</li>
            <li><strong>Key Entities:</strong> Mention important nouns (Customer, Transaction, Asset, etc.)</li>
            <li><strong>Relationships:</strong> Describe how entities relate to each other</li>
            <li><strong>Validation Needs:</strong> What rules or constraints must be enforced?</li>
            <li><strong>Use Case:</strong> How will this data be used? (queries, analysis, reporting)</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}
