#!/usr/bin/env python3
"""
Test suite for Day 4 evaluation system

Tests data loading, validation, and evaluation logic.
"""

import json
import os
import tempfile
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from backend.routers.day4.models import (
    EvaluationItem,
    JudgeResponse,
    EvaluationResult,
    EvaluationData,
)
from backend.routers.day4.evaluate import (
    load_evaluation_data,
    create_system_prompt,
    create_user_prompt,
    call_llm_judge,
    evaluate_system,
    print_results,
    save_results,
)


class TestEvaluationDataLoading:
    """Test evaluation data loading and validation"""

    def test_load_valid_evaluation_data(self):
        """Test loading valid evaluation data"""
        test_data = [
            {
                "query": "Test question?",
                "answer": "Test answer",
                "page": "123",
                "result": "System answer",
            }
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            evaluation_data = load_evaluation_data(temp_path)
            assert len(evaluation_data.items) == 1
            assert evaluation_data.items[0].query == "Test question?"
            assert evaluation_data.items[0].answer == "Test answer"
            assert evaluation_data.items[0].page == "123"
            assert evaluation_data.items[0].result == "System answer"
        finally:
            os.unlink(temp_path)

    def test_load_evaluation_data_with_items_wrapper(self):
        """Test loading evaluation data with items wrapper"""
        test_data = {
            "items": [
                {
                    "query": "Test question?",
                    "answer": "Test answer",
                    "page": "123",
                    "result": "System answer",
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            evaluation_data = load_evaluation_data(temp_path)
            assert len(evaluation_data.items) == 1
            assert evaluation_data.items[0].query == "Test question?"
        finally:
            os.unlink(temp_path)

    def test_load_nonexistent_file(self):
        """Test loading non-existent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            load_evaluation_data("nonexistent_file.json")

    def test_load_invalid_json(self):
        """Test loading invalid JSON raises ValueError"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content")
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Invalid JSON"):
                load_evaluation_data(temp_path)
        finally:
            os.unlink(temp_path)

    def test_load_missing_required_fields(self):
        """Test loading data with missing required fields"""
        test_data = [
            {
                "query": "Test question?",
                # missing answer, page, result
            }
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Invalid evaluation data format"):
                load_evaluation_data(temp_path)
        finally:
            os.unlink(temp_path)

    def test_load_empty_data(self):
        """Test loading empty data"""
        test_data = []

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            evaluation_data = load_evaluation_data(temp_path)
            assert len(evaluation_data.items) == 0
        finally:
            os.unlink(temp_path)


class TestJudgePrompt:
    """Test judge prompt creation"""

    def test_create_system_prompt(self):
        """Test system prompt creation"""
        system_prompt = create_system_prompt()

        assert "grader" in system_prompt
        assert "Tesla" in system_prompt
        assert "JSON" in system_prompt
        assert "correct" in system_prompt
        assert "reasoning" in system_prompt
        assert "factual" in system_prompt

    def test_create_user_prompt(self):
        """Test user prompt creation"""
        query = "Test question?"
        ground_truth = "Ground truth answer"
        system_answer = "System answer"

        user_prompt = create_user_prompt(query, ground_truth, system_answer)

        assert query in user_prompt
        assert ground_truth in user_prompt
        assert system_answer in user_prompt
        assert "Question:" in user_prompt
        assert "Reference Answer" in user_prompt
        assert "System Answer" in user_prompt

    def test_prompt_structure(self):
        """Test that prompts follow best practices"""
        system_prompt = create_system_prompt()
        user_prompt = create_user_prompt("Test?", "Answer", "Result")

        # System prompt should be instructional
        assert "You are" in system_prompt
        assert "Scoring" in system_prompt
        assert "Rules" in system_prompt

        # User prompt should be data-focused
        assert "Please evaluate" in user_prompt
        assert "JSON format" in user_prompt


class TestJudgeResponseModel:
    """Test JudgeResponse model and structured output functionality"""

    def test_judge_response_validation(self):
        """Test JudgeResponse model validation"""
        # Valid response
        response = JudgeResponse(correct=1, reasoning="Test reasoning")
        assert response.correct == 1
        assert response.reasoning == "Test reasoning"

        # Test field constraints
        with pytest.raises(ValueError):
            JudgeResponse(correct=2, reasoning="Invalid score")  # Score > 1

        with pytest.raises(ValueError):
            JudgeResponse(correct=-1, reasoning="Invalid score")  # Score < 0

    def test_get_json_schema_for_openrouter(self):
        """Test JSON schema generation for OpenRouter"""
        schema = JudgeResponse.get_json_schema_for_openrouter()

        assert schema["type"] == "object"
        assert "correct" in schema["properties"]
        assert "reasoning" in schema["properties"]
        assert schema["required"] == ["correct", "reasoning"]
        assert schema["additionalProperties"] is False

        # Test correct field constraints
        correct_field = schema["properties"]["correct"]
        assert correct_field["type"] == "integer"
        assert correct_field["minimum"] == 0
        assert correct_field["maximum"] == 1

        # Test reasoning field constraints
        reasoning_field = schema["properties"]["reasoning"]
        assert reasoning_field["type"] == "string"
        assert reasoning_field["maxLength"] == 200

    def test_get_openrouter_response_format(self):
        """Test complete response format for OpenRouter API"""
        response_format = JudgeResponse.get_openrouter_response_format()

        assert response_format["type"] == "json_schema"
        assert "json_schema" in response_format

        json_schema = response_format["json_schema"]
        assert json_schema["name"] == "judge_response"
        assert json_schema["strict"] is True
        assert "schema" in json_schema


class TestLLMJudge:
    """Test LLM judge functionality with mocked OpenAI calls"""

    @patch("backend.routers.day4.evaluate.OpenAI")
    def test_call_llm_judge_structured_output_success(self, mock_openai_class):
        """Test successful LLM judge call with structured outputs"""
        # Mock the OpenAI client and response
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[
            0
        ].message.content = '{"correct": 1, "reasoning": "Test reasoning"}'
        mock_client.chat.completions.create.return_value = mock_response

        # Call the function with structured output
        result = call_llm_judge(
            mock_client, "Test question", "Ground truth", "System answer", use_structured_output=True
        )

        # Verify result
        assert isinstance(result, JudgeResponse)
        assert result.correct == 1
        assert result.reasoning == "Test reasoning"

        # Verify that structured output format was used
        call_args = mock_client.chat.completions.create.call_args
        assert "response_format" in call_args.kwargs
        response_format = call_args.kwargs["response_format"]
        assert response_format["type"] == "json_schema"
        assert "json_schema" in response_format
        assert response_format["json_schema"]["strict"] is True

    @patch("backend.routers.day4.evaluate.OpenAI")
    def test_call_llm_judge_fallback_success(self, mock_openai_class):
        """Test successful LLM judge call with fallback mode"""
        # Mock the OpenAI client and response
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[
            0
        ].message.content = '{"correct": 1, "reasoning": "Test reasoning"}'
        mock_client.chat.completions.create.return_value = mock_response

        # Call the function with fallback mode
        result = call_llm_judge(
            mock_client, "Test question", "Ground truth", "System answer", use_structured_output=False
        )

        # Verify result
        assert isinstance(result, JudgeResponse)
        assert result.correct == 1
        assert result.reasoning == "Test reasoning"

        # Verify that basic JSON format was used
        call_args = mock_client.chat.completions.create.call_args
        assert "response_format" in call_args.kwargs
        response_format = call_args.kwargs["response_format"]
        assert response_format == {"type": "json_object"}

    @patch("backend.routers.day4.evaluate.OpenAI")
    def test_call_llm_judge_json_error_fallback_mode(self, mock_openai_class):
        """Test LLM judge call with JSON parsing error in fallback mode"""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "invalid json"
        mock_client.chat.completions.create.return_value = mock_response

        result = call_llm_judge(
            mock_client, "Test question", "Ground truth", "System answer", use_structured_output=False
        )

        # Should return failure response
        assert result.correct == 0
        assert "JSON parsing failed" in result.reasoning

    @patch("backend.routers.day4.evaluate.OpenAI")
    def test_call_llm_judge_api_error(self, mock_openai_class):
        """Test LLM judge call with API error"""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        result = call_llm_judge(
            mock_client, "Test question", "Ground truth", "System answer", use_structured_output=False
        )

        # Should return failure response
        assert result.correct == 0
        assert "API call failed" in result.reasoning

    @patch("backend.routers.day4.evaluate.OpenAI")
    def test_call_llm_judge_structured_output_fallback(self, mock_openai_class):
        """Test automatic fallback when structured output is not supported"""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        # First call fails with schema error, second succeeds
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"correct": 1, "reasoning": "Fallback worked"}'

        mock_client.chat.completions.create.side_effect = [
            Exception("json_schema not supported"),  # First call with structured output fails
            mock_response  # Second call with fallback succeeds
        ]

        result = call_llm_judge(
            mock_client, "Test question", "Ground truth", "System answer", use_structured_output=True
        )

        # Should return success after fallback
        assert result.correct == 1
        assert result.reasoning == "Fallback worked"

        # Should have been called twice (once for structured, once for fallback)
        assert mock_client.chat.completions.create.call_count == 2


class TestEvaluationSystem:
    """Test the complete evaluation system"""

    @patch("backend.routers.day4.evaluate.call_llm_judge")
    def test_evaluate_system(self, mock_judge):
        """Test complete system evaluation"""
        # Mock judge responses
        mock_judge.side_effect = [
            JudgeResponse(correct=1, reasoning="Correct answer"),
            JudgeResponse(correct=0, reasoning="Incorrect answer"),
            JudgeResponse(correct=1, reasoning="Another correct answer"),
        ]

        # Create test data
        evaluation_data = EvaluationData(
            items=[
                EvaluationItem(query="Q1", answer="A1", page="P1", result="R1"),
                EvaluationItem(query="Q2", answer="A2", page="P2", result="R2"),
                EvaluationItem(query="Q3", answer="A3", page="P3", result="R3"),
            ]
        )

        # Evaluate system
        results = evaluate_system(evaluation_data, "fake_api_key")

        # Verify results
        assert results.total_questions == 3
        assert results.correct_answers == 2
        assert results.accuracy == 2 / 3
        assert len(results.detailed_results) == 3

        # Check first result
        first_result = results.detailed_results[0]
        assert first_result["query"] == "Q1"
        assert first_result["correct"] == 1
        assert first_result["reasoning"] == "Correct answer"

    def test_evaluate_empty_system(self):
        """Test evaluation with empty data"""
        evaluation_data = EvaluationData(items=[])
        results = evaluate_system(evaluation_data, "fake_api_key")

        assert results.total_questions == 0
        assert results.correct_answers == 0
        assert results.accuracy == 0.0
        assert len(results.detailed_results) == 0


class TestResultsHandling:
    """Test results printing and saving"""

    def test_save_results(self):
        """Test saving results to file"""
        results = EvaluationResult(
            total_questions=2,
            correct_answers=1,
            accuracy=0.5,
            detailed_results=[{"question_id": 1, "correct": 1, "reasoning": "Good"}],
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            save_results(results, temp_path)

            # Verify file was created and contains correct data
            assert os.path.exists(temp_path)
            with open(temp_path, "r") as f:
                saved_data = json.load(f)

            assert saved_data["total_questions"] == 2
            assert saved_data["correct_answers"] == 1
            assert saved_data["accuracy"] == 0.5
        finally:
            os.unlink(temp_path)

    def test_print_results(self, capsys):
        """Test printing results (capture stdout)"""
        results = EvaluationResult(
            total_questions=1,
            correct_answers=1,
            accuracy=1.0,
            detailed_results=[
                {
                    "question_id": 1,
                    "query": "Test query",
                    "ground_truth": "Test truth",
                    "system_answer": "Test answer",
                    "page": "123",
                    "correct": 1,
                    "reasoning": "Correct!",
                }
            ],
        )

        print_results(results)
        captured = capsys.readouterr()

        assert "EVALUATION RESULTS" in captured.out
        assert "Total Questions: 1" in captured.out
        assert "Correct Answers: 1" in captured.out
        assert "Accuracy: 100.00%" in captured.out
        assert "✓ CORRECT" in captured.out


class TestIntegration:
    """Integration tests using test sample data"""

    def test_load_sample_data(self):
        """Test loading the sample test data"""
        sample_path = Path(__file__).parent / "test_data_sample.json"

        # Sample file should exist
        assert sample_path.exists()

        # Should load successfully
        evaluation_data = load_evaluation_data(str(sample_path))
        assert len(evaluation_data.items) > 0

        # All items should have required fields
        for item in evaluation_data.items:
            assert item.query
            assert item.answer
            assert item.page
            assert item.result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
