'use client'

/**
 * File System Browser - Learning Center Component
 *
 * Browses and displays pydantic_library directory structure.
 * Allows viewing file contents with syntax highlighting.
 */

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import {
  Folder,
  File,
  FileCode,
  FileText,
  FileJson,
  ChevronRight,
  ChevronDown,
  Download,
  Eye,
  FolderOpen
} from 'lucide-react'

interface FileNode {
  name: string
  path: string
  type: 'file' | 'directory'
  size: number | null
  extension: string | null
  children?: FileNode[]
}

interface FileContent {
  path: string
  content: string
  size: number
  extension: string
  language: string
}

interface FileSystemBrowserProps {
  initialPath?: string
}

export default function FileSystemBrowser({ initialPath = '/' }: FileSystemBrowserProps) {
  const [currentPath, setCurrentPath] = useState(initialPath)
  const [nodes, setNodes] = useState<FileNode[]>([])
  const [expandedPaths, setExpandedPaths] = useState<Set<string>>(new Set(['/']))
  const [selectedFile, setSelectedFile] = useState<FileContent | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isDialogOpen, setIsDialogOpen] = useState(false)

  // Fetch directory contents
  const fetchDirectory = async (path: string) => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(
        `http://localhost:8000/api/learning-center/files/browse?path=${encodeURIComponent(path)}`
      )

      if (!response.ok) {
        throw new Error(`Failed to fetch directory: ${response.statusText}`)
      }

      const data: FileNode[] = await response.json()
      return data
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to load directory'
      setError(errorMsg)
      console.error('Error fetching directory:', err)
      return []
    } finally {
      setIsLoading(false)
    }
  }

  // Fetch file content
  const fetchFile = async (path: string) => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(
        `http://localhost:8000/api/learning-center/files/read?path=${encodeURIComponent(path)}`
      )

      if (!response.ok) {
        throw new Error(`Failed to fetch file: ${response.statusText}`)
      }

      const data: FileContent = await response.json()
      setSelectedFile(data)
      setIsDialogOpen(true)
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to load file'
      setError(errorMsg)
      console.error('Error fetching file:', err)
    } finally {
      setIsLoading(false)
    }
  }

  // Load initial directory
  useEffect(() => {
    fetchDirectory(currentPath).then((data) => setNodes(data))
  }, [currentPath])

  // Toggle directory expansion
  const toggleExpanded = (path: string) => {
    const newExpanded = new Set(expandedPaths)
    if (newExpanded.has(path)) {
      newExpanded.delete(path)
    } else {
      newExpanded.add(path)
    }
    setExpandedPaths(newExpanded)
  }

  // Handle file click
  const handleFileClick = (node: FileNode) => {
    if (node.type === 'directory') {
      toggleExpanded(node.path)
      if (!expandedPaths.has(node.path)) {
        // Load children when expanding
        fetchDirectory(node.path)
      }
    } else {
      fetchFile(node.path)
    }
  }

  // Get file icon based on extension
  const getFileIcon = (node: FileNode) => {
    if (node.type === 'directory') {
      return expandedPaths.has(node.path) ? (
        <FolderOpen className="w-4 h-4 text-yellow-500" />
      ) : (
        <Folder className="w-4 h-4 text-yellow-500" />
      )
    }

    const ext = node.extension?.toLowerCase()
    if (ext === '.py') return <FileCode className="w-4 h-4 text-blue-500" />
    if (ext === '.yaml' || ext === '.yml') return <FileText className="w-4 h-4 text-orange-500" />
    if (ext === '.json') return <FileJson className="w-4 h-4 text-green-500" />
    if (ext === '.md') return <FileText className="w-4 h-4 text-gray-500" />

    return <File className="w-4 h-4 text-gray-500" />
  }

  // Format file size
  const formatSize = (bytes: number | null) => {
    if (bytes === null) return ''
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  // Download file
  const handleDownload = () => {
    if (!selectedFile) return

    const blob = new Blob([selectedFile.content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = selectedFile.path.split('/').pop() || 'file.txt'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  // Render file node
  const renderNode = (node: FileNode, depth: number = 0) => {
    const isExpanded = expandedPaths.has(node.path)

    return (
      <div key={node.path}>
        <button
          onClick={() => handleFileClick(node)}
          className="flex items-center gap-2 w-full px-2 py-1 hover:bg-accent rounded text-sm transition-colors"
          style={{ paddingLeft: `${depth * 16 + 8}px` }}
        >
          {node.type === 'directory' && (
            <span className="shrink-0">
              {isExpanded ? (
                <ChevronDown className="w-3 h-3" />
              ) : (
                <ChevronRight className="w-3 h-3" />
              )}
            </span>
          )}
          {getFileIcon(node)}
          <span className="flex-1 text-left truncate">{node.name}</span>
          {node.size !== null && (
            <Badge variant="secondary" className="text-xs">
              {formatSize(node.size)}
            </Badge>
          )}
        </button>

        {node.type === 'directory' && isExpanded && node.children && (
          <div>
            {node.children.map((child) => renderNode(child, depth + 1))}
          </div>
        )}
      </div>
    )
  }

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Folder className="w-5 h-5 text-primary" />
            File System Browser
          </CardTitle>
          <CardDescription className="text-sm">
            pydantic_library/
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="text-red-500 text-sm p-2 bg-red-50 dark:bg-red-950 rounded mb-2">
              {error}
            </div>
          )}

          {isLoading && nodes.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              Loading files...
            </div>
          )}

          <ScrollArea className="h-96 pr-4">
            <div className="space-y-1">
              {nodes.map((node) => renderNode(node))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>

      {/* File Viewer Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-4xl max-h-[80vh]">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <FileCode className="w-5 h-5" />
              {selectedFile?.path}
            </DialogTitle>
            <DialogDescription className="flex items-center gap-2">
              <Badge variant="secondary">{selectedFile?.language}</Badge>
              <Badge variant="secondary">{formatSize(selectedFile?.size || 0)}</Badge>
            </DialogDescription>
          </DialogHeader>

          <ScrollArea className="h-[60vh] w-full">
            <pre className="text-xs font-mono p-4 bg-muted rounded">
              <code>{selectedFile?.content}</code>
            </pre>
          </ScrollArea>

          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={handleDownload}>
              <Download className="w-4 h-4 mr-2" />
              Download
            </Button>
            <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
              Close
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}
