from django.shortcuts import render
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
import google.generativeai as genai
import ast
import subprocess
import tempfile

genai.configure(api_key="AIzaSyCPX2ec_fLRVWud9IQ8tCuG6iS-YwRdft0")
model = genai.GenerativeModel('gemini-2.5-pro')

@api_view(['POST'])
def analyze_code(request):
    code = request.data.get('code','')
    language = request.data.get('language', 'python')

    if not code:
        return Response({'error': 'No code provided'}, status=400)
    
    explanation = ''
    errors = []
    suggestions = []

    try:
        prompt = f"Explain this {language} code in detail: \n \n{code}"
        response = model.generate_content(prompt)
        explanation = response.text.strip()

        if language == 'python':
            try:
                ast.parse(code)
            except Exception as e:
                errors.append(str(e))

            with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as temp:
                temp.write(code)
                temp.flush()
                result = subprocess.run(
                    ['pylint', temp.name, '--disable=all', '--enable=E,W,R,C'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                suggestions = result.stdout.splitlines()

    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
    return Response({
        'explanation': explanation,
        'errors': errors,
        'suggestions': suggestions,
    })


