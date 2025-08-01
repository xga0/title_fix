import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Copy, Check, Type, BarChart3, Hash, Zap } from 'lucide-react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [caseType, setCaseType] = useState('title'); // Fixed root cause, safe to start with title case
  const [style, setStyle] = useState('apa');
  const [straightQuotes, setStraightQuotes] = useState(false);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState(null);
  const [optionsLoaded, setOptionsLoaded] = useState(false);
  const [options, setOptions] = useState({
    supported_styles: ['apa', 'chicago', 'ap', 'mla', 'nyt'], // Provide defaults
    supported_case_types: ['title', 'sentence', 'upper', 'lower', 'first', 'alt', 'toggle']
  });

  const fetchOptions = async () => {
    try {
      const response = await axios.get('/api/options');
      setOptions(response.data);
      setOptionsLoaded(true);
    } catch (error) {
      console.error('Error fetching options:', error);
      // Keep default options if fetch fails
      setOptionsLoaded(true);
    }
  };

  // Conversion function - no useCallback to avoid circular dependencies
  const convertText = async (textToConvert, caseTypeToUse, styleToUse, straightQuotesToUse) => {
    if (!textToConvert.trim()) return;

    // Prevent sending requests with invalid/empty case types
    if (!caseTypeToUse || caseTypeToUse === '') {
      console.log('Skipping conversion - no case type selected');
      return;
    }

    setLoading(true);
    setError(null); // Clear any previous errors
    
    try {
      const response = await axios.post('/api/convert', {
        text: textToConvert,
        case_type: caseTypeToUse,
        style: styleToUse,
        straight_quotes: straightQuotesToUse,
        quick_copy: true
      });
      
      // Validate response structure and clean up data
      if (response.data && typeof response.data === 'object') {
        const cleanedResult = {
          ...response.data,
          style: response.data.style || (caseTypeToUse === 'title' ? styleToUse : null),
          case_type: response.data.case_type || caseTypeToUse
        };
        setResult(cleanedResult);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      console.error('Error converting text:', error);
      setError(error.message || 'Conversion failed');
      if (error.response?.data?.detail) {
        console.error('API Error details:', error.response.data.detail);
      }
      setResult({
        text: 'Error converting text. Please try again.',
        word_count: 0,
        char_count: 0,
        headline_score: 0,
        case_type: caseTypeToUse,
        style: caseTypeToUse === 'title' ? styleToUse : null
      });
    } finally {
      setLoading(false);
    }
  };

  // Fetch supported options on component mount
  useEffect(() => {
    fetchOptions();
  }, []);

  // Convert text whenever input changes (with debouncing) - clean separation of concerns
  useEffect(() => {
    if (!text.trim()) {
      setResult(null);
      return;
    }

    const timer = setTimeout(() => {
      convertText(text, caseType, style, straightQuotes);
    }, 300); // 300ms debounce

    return () => clearTimeout(timer);
  }, [text, caseType, style, straightQuotes]); // Clean dependencies, no function references

  const copyToClipboard = async () => {
    if (result?.text) {
      try {
        await navigator.clipboard.writeText(result.text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      } catch (error) {
        console.error('Failed to copy:', error);
      }
    }
  };

  const getCaseTypeDisplayName = (type) => {
    // Handle all falsy values (null, undefined, empty string)
    if (!type || type === null || type === undefined) {
      return 'Unknown Case';
    }
    const names = {
      title: 'Title Case',
      sentence: 'Sentence case',
      upper: 'UPPERCASE',
      lower: 'lowercase',
      first: 'First Letter Case',
      alt: 'AlTeRnAtInG cAsE',
      toggle: 'tOGGLE cAsE'
    };
    return names[type] || String(type);
  };

  const getStyleDisplayName = (styleCode) => {
    // Handle all falsy values (null, undefined, empty string)
    if (!styleCode || styleCode === null || styleCode === undefined) {
      return 'Unknown Style';
    }
    const names = {
      apa: 'APA Style',
      chicago: 'Chicago Style',
      ap: 'AP Style',
      mla: 'MLA Style',
      nyt: 'NYT Style'
    };
    return names[styleCode] || String(styleCode).toUpperCase();
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  // Error boundary fallback
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-6 max-w-md">
          <h2 className="text-lg font-semibold text-red-600 mb-2">Application Error</h2>
          <p className="text-gray-700 mb-4">{error}</p>
          <button 
            onClick={() => {setError(null); window.location.reload();}} 
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Reload App
          </button>
        </div>
      </div>
    );
  }

  // Don't render until options are loaded to prevent crashes
  if (!optionsLoaded) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-lg">Loading...</p>
        </div>
      </div>
    );
  }

  try {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="flex items-center space-x-3">
            <Type className="h-8 w-8 text-indigo-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Title Fix</h1>
              <p className="text-gray-600">Intelligent title case conversion and text formatting</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <label htmlFor="text-input" className="block text-sm font-medium text-gray-700 mb-2">
            Enter your text:
          </label>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type or paste your text here to convert it..."
            className="w-full h-32 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
          />
          
          {/* Options */}
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Case Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Case Type</label>
              <select
                value={caseType}
                onChange={(e) => {
                  try {
                    const newCaseType = e.target.value;
                    
                    // If switching to title case, ensure we have a valid style
                    if (newCaseType === 'title' && !options.supported_styles.includes(style)) {
                      setStyle(options.supported_styles[0] || 'apa');
                    }
                    
                    setCaseType(newCaseType);
                  } catch (err) {
                    console.error('Error changing case type:', err);
                    setError('Error changing case type: ' + err.message);
                  }
                }}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                {options.supported_case_types.map((type) => {
                  try {
                    return (
                      <option key={type} value={type}>
                        {getCaseTypeDisplayName(type)}
                      </option>
                    );
                  } catch (err) {
                    console.error('Error rendering case type option:', type, err);
                    return null;
                  }
                })}
              </select>
            </div>

            {/* Style (only for title case) */}
            {caseType === 'title' && optionsLoaded && options.supported_styles && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Citation Style</label>
                <select
                  value={options.supported_styles.includes(style) ? style : options.supported_styles[0] || 'apa'}
                  onChange={(e) => setStyle(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                >
                  {options.supported_styles.map((styleOption) => {
                    try {
                      return (
                        <option key={styleOption} value={styleOption}>
                          {getStyleDisplayName(styleOption)}
                        </option>
                      );
                    } catch (err) {
                      console.error('Error rendering style option:', styleOption, err);
                      return null;
                    }
                  })}
                </select>
              </div>
            )}

            {/* Straight Quotes */}
            <div className="flex items-center">
              <input
                type="checkbox"
                id="straight-quotes"
                checked={straightQuotes}
                onChange={(e) => setStraightQuotes(e.target.checked)}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="straight-quotes" className="ml-2 text-sm text-gray-700">
                Convert to straight quotes
              </label>
            </div>
          </div>
        </div>

        {/* Result Section */}
        {(result || loading) && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Result</h2>
              {result && (
                <button
                  onClick={copyToClipboard}
                  className="flex items-center space-x-2 px-3 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
                >
                  {copied ? (
                    <>
                      <Check className="h-4 w-4" />
                      <span>Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="h-4 w-4" />
                      <span>Copy</span>
                    </>
                  )}
                </button>
              )}
            </div>

            {loading ? (
              <div className="flex items-center justify-center h-20">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
              </div>
            ) : result ? (
              <>
                <div className="bg-gray-50 rounded-md p-4 mb-4">
                  <p className="text-lg leading-relaxed text-gray-900">{result.text}</p>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center p-3 bg-blue-50 rounded-lg">
                    <Hash className="h-5 w-5 text-blue-600 mx-auto mb-1" />
                    <p className="text-sm text-gray-600">Words</p>
                    <p className="text-xl font-bold text-blue-600">{result.word_count}</p>
                  </div>
                  
                  <div className="text-center p-3 bg-green-50 rounded-lg">
                    <Type className="h-5 w-5 text-green-600 mx-auto mb-1" />
                    <p className="text-sm text-gray-600">Characters</p>
                    <p className="text-xl font-bold text-green-600">{result.char_count}</p>
                  </div>
                  
                  <div className="text-center p-3 bg-purple-50 rounded-lg">
                    <BarChart3 className="h-5 w-5 text-purple-600 mx-auto mb-1" />
                    <p className="text-sm text-gray-600">Headline Score</p>
                    <p className={`text-xl font-bold ${getScoreColor(result.headline_score)}`}>
                      {result.headline_score}
                    </p>
                  </div>
                  
                  <div className="text-center p-3 bg-orange-50 rounded-lg">
                    <Zap className="h-5 w-5 text-orange-600 mx-auto mb-1" />
                    <p className="text-sm text-gray-600">Style</p>
                    <p className="text-sm font-bold text-orange-600">
                      {(() => {
                        try {
                          if (caseType === 'title') {
                            const styleToDisplay = result?.style || style || 'apa';
                            return getStyleDisplayName(styleToDisplay);
                          } else {
                            const caseToDisplay = result?.case_type || caseType || 'sentence';
                            return getCaseTypeDisplayName(caseToDisplay);
                          }
                        } catch (err) {
                          console.error('Error displaying style/case:', err);
                          return 'Display Error';
                        }
                      })()}
                    </p>
                  </div>
                </div>
              </>
            ) : null}
          </div>
        )}

        {/* Help Section */}
        {!text && (
          <div className="bg-white rounded-lg shadow-md p-6 mt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">How to Use</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Case Types</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li><strong>Title Case:</strong> Proper capitalization following citation styles</li>
                  <li><strong>Sentence case:</strong> Only first word and proper nouns capitalized</li>
                  <li><strong>UPPERCASE:</strong> All letters capitalized</li>
                  <li><strong>lowercase:</strong> All letters lowercase</li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Citation Styles</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li><strong>APA:</strong> American Psychological Association</li>
                  <li><strong>Chicago:</strong> Chicago Manual of Style</li>
                  <li><strong>AP:</strong> Associated Press</li>
                  <li><strong>MLA:</strong> Modern Language Association</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <p className="text-center text-gray-600">
            Built with ❤️ using the Title Fix Python package
          </p>
        </div>
      </footer>
    </div>
  );
  } catch (renderError) {
    console.error('React render error:', renderError);
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-6 max-w-md">
          <h2 className="text-lg font-semibold text-red-600 mb-2">Render Error</h2>
          <p className="text-gray-700 mb-4">Something went wrong. Please refresh the page.</p>
          <button 
            onClick={() => window.location.reload()} 
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Refresh Page
          </button>
        </div>
      </div>
    );
  }
}

export default App; 