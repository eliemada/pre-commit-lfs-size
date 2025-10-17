"""Unit tests for check_lfs_size.py."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from check_lfs_size import (
    bytes_to_mb,
    check_lfs_file_sizes,
    get_file_size,
    get_staged_files,
    is_tracked_by_lfs,
    main,
)


class TestGetStagedFiles:
    """Tests for get_staged_files function."""

    @patch("check_lfs_size.subprocess.check_output")
    def test_returns_staged_files(self, mock_check_output) -> None:
        """Test that staged files are returned as Path objects."""
        mock_check_output.return_value = "file1.txt\nfile2.py\nfile3.md\n"
        result = get_staged_files()

        assert result == [Path("file1.txt"), Path("file2.py"), Path("file3.md")]
        mock_check_output.assert_called_once_with(
            ["/usr/bin/git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
            text=True,
        )

    @patch("check_lfs_size.subprocess.check_output")
    def test_handles_empty_output(self, mock_check_output) -> None:
        """Test handling of no staged files."""
        mock_check_output.return_value = ""
        result = get_staged_files()

        assert result == []

    @patch("check_lfs_size.subprocess.check_output")
    def test_handles_subprocess_error(self, mock_check_output) -> None:
        """Test handling of subprocess errors."""
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")
        result = get_staged_files()

        assert result == []

    @patch("check_lfs_size.subprocess.check_output")
    def test_strips_whitespace(self, mock_check_output) -> None:
        """Test that whitespace is stripped from file names."""
        mock_check_output.return_value = "  file1.txt  \n  file2.py  \n"
        result = get_staged_files()

        assert result == [Path("file1.txt"), Path("file2.py")]


class TestIsTrackedByLfs:
    """Tests for is_tracked_by_lfs function."""

    @patch("check_lfs_size.subprocess.check_output")
    def test_file_tracked_by_lfs(self, mock_check_output) -> None:
        """Test detection of LFS-tracked files."""
        mock_check_output.return_value = "file.txt: filter: lfs"
        result = is_tracked_by_lfs(Path("file.txt"))

        assert result is True
        mock_check_output.assert_called_once_with(
            ["/usr/bin/git", "check-attr", "filter", "file.txt"],
            text=True,
        )

    @patch("check_lfs_size.subprocess.check_output")
    def test_file_not_tracked_by_lfs(self, mock_check_output) -> None:
        """Test detection of non-LFS files."""
        mock_check_output.return_value = "file.txt: filter: unspecified"
        result = is_tracked_by_lfs(Path("file.txt"))

        assert result is False

    @patch("check_lfs_size.subprocess.check_output")
    def test_handles_subprocess_error(self, mock_check_output) -> None:
        """Test handling of subprocess errors."""
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")
        result = is_tracked_by_lfs(Path("file.txt"))

        assert result is False


class TestGetFileSize:
    """Tests for get_file_size function."""

    def test_returns_file_size(self, tmp_path) -> None:
        """Test that file size is returned in bytes."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")
        size = get_file_size(test_file)

        assert size == 13  # "Hello, World!" is 13 bytes

    def test_large_file(self, tmp_path) -> None:
        """Test handling of larger files."""
        test_file = tmp_path / "large.bin"
        test_file.write_bytes(b"X" * 1024 * 1024)  # 1 MB
        size = get_file_size(test_file)

        assert size == 1024 * 1024


class TestBytesToMb:
    """Tests for bytes_to_mb function."""

    def test_converts_bytes_to_mb(self) -> None:
        """Test conversion from bytes to megabytes."""
        assert bytes_to_mb(1024 * 1024) == 1.0
        assert bytes_to_mb(1024 * 1024 * 10) == 10.0
        assert bytes_to_mb(1024 * 1024 * 50) == 50.0

    def test_rounds_to_two_decimals(self) -> None:
        """Test that result is rounded to 2 decimal places."""
        assert bytes_to_mb(1024 * 1024 * 1.5) == 1.5
        assert bytes_to_mb(1536 * 1024) == 1.5
        assert bytes_to_mb(1234567) == 1.18

    def test_handles_zero(self) -> None:
        """Test conversion of zero bytes."""
        assert bytes_to_mb(0) == 0.0


class TestCheckLfsFileSizes:
    """Tests for check_lfs_file_sizes function."""

    @patch("check_lfs_size.get_staged_files")
    def test_no_staged_files(self, mock_get_staged) -> None:
        """Test when there are no staged files."""
        mock_get_staged.return_value = []
        result = check_lfs_file_sizes(50.0)

        assert result == 0

    @patch("check_lfs_size.get_staged_files")
    @patch("check_lfs_size.is_tracked_by_lfs")
    @patch("check_lfs_size.get_file_size")
    def test_lfs_file_within_limit(
        self, mock_get_size, mock_is_lfs, mock_get_staged, tmp_path
    ) -> None:
        """Test LFS file within size limit."""
        test_file = tmp_path / "small.bin"
        test_file.write_bytes(b"X" * 1024)  # 1 KB

        mock_get_staged.return_value = [test_file]
        mock_is_lfs.return_value = True
        mock_get_size.return_value = 1024  # 1 KB

        result = check_lfs_file_sizes(50.0)

        assert result == 0

    @patch("check_lfs_size.get_staged_files")
    @patch("check_lfs_size.is_tracked_by_lfs")
    @patch("check_lfs_size.get_file_size")
    @patch("builtins.print")
    def test_lfs_file_exceeds_limit(
        self, mock_print, mock_get_size, mock_is_lfs, mock_get_staged, tmp_path
    ) -> None:
        """Test LFS file exceeding size limit."""
        test_file = tmp_path / "large.bin"
        test_file.write_bytes(b"X")

        mock_get_staged.return_value = [test_file]
        mock_is_lfs.return_value = True
        mock_get_size.return_value = 100 * 1024 * 1024  # 100 MB

        result = check_lfs_file_sizes(50.0)

        assert result == 1
        assert mock_print.call_count == 2  # Error message + file details

    @patch("check_lfs_size.get_staged_files")
    @patch("check_lfs_size.is_tracked_by_lfs")
    def test_non_lfs_file_ignored(self, mock_is_lfs, mock_get_staged, tmp_path) -> None:
        """Test that non-LFS files are ignored."""
        test_file = tmp_path / "regular.txt"
        test_file.write_text("Regular file")

        mock_get_staged.return_value = [test_file]
        mock_is_lfs.return_value = False

        result = check_lfs_file_sizes(50.0)

        assert result == 0

    @patch("check_lfs_size.get_staged_files")
    @patch("check_lfs_size.is_tracked_by_lfs")
    @patch("check_lfs_size.get_file_size")
    @patch("builtins.print")
    def test_multiple_oversized_files(
        self, mock_print, mock_get_size, mock_is_lfs, mock_get_staged, tmp_path
    ) -> None:
        """Test multiple files exceeding size limit."""
        file1 = tmp_path / "file1.bin"
        file2 = tmp_path / "file2.bin"
        file1.write_bytes(b"X")
        file2.write_bytes(b"X")

        mock_get_staged.return_value = [file1, file2]
        mock_is_lfs.return_value = True
        mock_get_size.return_value = 100 * 1024 * 1024  # 100 MB

        result = check_lfs_file_sizes(50.0)

        assert result == 1
        assert mock_print.call_count == 3  # Error header + 2 files

    @patch("check_lfs_size.get_staged_files")
    def test_nonexistent_file_ignored(self, mock_get_staged) -> None:
        """Test that non-existent files are skipped."""
        mock_get_staged.return_value = [Path("nonexistent.txt")]
        result = check_lfs_file_sizes(50.0)

        assert result == 0


class TestMain:
    """Tests for main function."""

    @patch("sys.argv", ["check_lfs_size.py"])
    @patch("check_lfs_size.check_lfs_file_sizes")
    def test_default_max_size(self, mock_check) -> None:
        """Test that default max size is 50 MB."""
        mock_check.return_value = 0
        result = main()

        mock_check.assert_called_once_with(50.0)
        assert result == 0

    @patch("sys.argv", ["check_lfs_size.py", "--max-size", "100"])
    @patch("check_lfs_size.check_lfs_file_sizes")
    def test_custom_max_size(self, mock_check) -> None:
        """Test custom max size argument."""
        mock_check.return_value = 0
        result = main()

        mock_check.assert_called_once_with(100.0)
        assert result == 0

    @patch("sys.argv", ["check_lfs_size.py", "--max-size", "25.5"])
    @patch("check_lfs_size.check_lfs_file_sizes")
    def test_fractional_max_size(self, mock_check) -> None:
        """Test fractional max size argument."""
        mock_check.return_value = 0
        result = main()

        mock_check.assert_called_once_with(25.5)
        assert result == 0

    @patch("sys.argv", ["check_lfs_size.py"])
    @patch("check_lfs_size.check_lfs_file_sizes")
    def test_returns_failure_code(self, mock_check) -> None:
        """Test that failure code is propagated."""
        mock_check.return_value = 1
        result = main()

        assert result == 1
