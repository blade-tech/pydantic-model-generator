import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, Sparkles, Brain, FileText, Database, Code, PlayCircle } from 'lucide-react'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 md:p-24">
      <div className="z-10 max-w-6xl w-full space-y-8">
        {/* Hero */}
        <div className="text-center space-y-4">
          <Badge className="mb-2">Live Demo</Badge>
          <h1 className="text-4xl md:text-5xl font-bold">
            Pydantic Model Generator
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto">
            Transform business outcomes into validated Pydantic models with AI-powered ontology mapping
          </p>
          <div className="flex gap-4 justify-center pt-4">
            <Link href="/workflow">
              <Button size="lg">
                Start Workflow
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
            <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">
              <Button variant="outline" size="lg">
                API Docs
              </Button>
            </a>
          </div>
        </div>

        {/* 6-Step Workflow Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <Badge>Step 1</Badge>
                <Sparkles className="w-5 h-5 text-muted-foreground" />
              </div>
              <CardTitle className="text-lg">Business Outcome</CardTitle>
              <CardDescription>Enter your use case or requirements</CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <Badge>Step 2</Badge>
                <Brain className="w-5 h-5 text-muted-foreground" />
              </div>
              <CardTitle className="text-lg">Ontology Research</CardTitle>
              <CardDescription>Claude maps entities to canonical ontologies</CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <Badge>Step 3</Badge>
                <FileText className="w-5 h-5 text-muted-foreground" />
              </div>
              <CardTitle className="text-lg">OutcomeSpec</CardTitle>
              <CardDescription>Generate outcome specification YAML</CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <Badge>Step 4</Badge>
                <Database className="w-5 h-5 text-muted-foreground" />
              </div>
              <CardTitle className="text-lg">LinkML Schema</CardTitle>
              <CardDescription>Generate LinkML schema with ontology URIs</CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <Badge>Step 5</Badge>
                <Code className="w-5 h-5 text-muted-foreground" />
              </div>
              <CardTitle className="text-lg">Pydantic Models</CardTitle>
              <CardDescription>Generate validated Pydantic V2 code</CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <Badge>Step 6</Badge>
                <PlayCircle className="w-5 h-5 text-muted-foreground" />
              </div>
              <CardTitle className="text-lg">Testing</CardTitle>
              <CardDescription>Run pytest and validate models</CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* Features */}
        <Card>
          <CardHeader>
            <CardTitle>Key Features</CardTitle>
          </CardHeader>
          <CardContent className="grid md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-semibold mb-2 text-sm">Real API Integration</h3>
              <p className="text-xs text-muted-foreground">
                No mocks - uses real Claude, OpenAI, and Neo4j APIs for production-ready results
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2 text-sm">Live AI Reasoning</h3>
              <p className="text-xs text-muted-foreground">
                Watch Claude think in real-time via Server-Sent Events streaming
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2 text-sm">Human-in-the-Loop</h3>
              <p className="text-xs text-muted-foreground">
                Approve or edit each transformation step before proceeding
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2 text-sm">File System Integration</h3>
              <p className="text-xs text-muted-foreground">
                Writes real files to pydantic_library with subprocess execution
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Warning */}
        <Card className="border-yellow-500">
          <CardContent className="p-4 text-center">
            <p className="text-sm text-yellow-600 dark:text-yellow-400">
              ⚠️ This app uses REAL API keys and makes REAL calls to Claude, OpenAI, and Neo4j.
              Make sure your .env file is configured before starting.
            </p>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}
