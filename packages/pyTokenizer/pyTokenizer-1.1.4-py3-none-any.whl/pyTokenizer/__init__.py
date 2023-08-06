# EMACS settings: -*- tab-width: 2; indent-tabs-mode: t -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# =============================================================================
#              _____     _              _
#   _ __  _   |_   _|__ | | _____ _ __ (_)_______ _ __
#  | '_ \| | | || |/ _ \| |/ / _ \ '_ \| |_  / _ \ '__|
#  | |_) | |_| || | (_) |   <  __/ | | | |/ /  __/ |
#  | .__/ \__, ||_|\___/|_|\_\___|_| |_|_/___\___|_|
#  |_|    |___/
# =============================================================================
# Authors:						Patrick Lehmann
#
# Python package:	    A streaming tokenizer.
#
# Description:
# ------------------------------------
#		TODO
#
# License:
# ============================================================================
# Copyright 2017-2020 Patrick Lehmann - Bötzingen, Germany
# Copyright 2007-2016 Patrick Lehmann - Dresden, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#
from enum import Enum


__api__ = [
	'ParserException',
	'MismatchingParserResult',
	'EmptyChoiseParserResult',
	'MatchingParserResult',
	'GreedyMatchingParserResult',
	'SourceCodePosition',
	'Token',
	'SuperToken',
	'ValuedToken',
	'StartOfDocumentToken',
	'CharacterToken',
	'SpaceToken',
	'DelimiterToken',
	'NumberToken',
	'StringToken',
	'Tokenizer'
]
__all__ = __api__


class ParserException(Exception):
	"""Base exception for all exceptions created by the Tokenizer."""

class MismatchingParserResult(StopIteration):             pass
class EmptyChoiseParserResult(MismatchingParserResult):   pass
class MatchingParserResult(StopIteration):                pass
class GreedyMatchingParserResult(MatchingParserResult):   pass


class SourceCodePosition:
	"""
	Represents a position in a source code file.

	The class offers a linear position: `Absolute` in bytes from document or
	snippet start and a ragged 2 dimensional `Row`:`Column` position.
	"""

	Row       : int = None    #: Row or line in the document
	Column    : int = None    #: Column in the document
	Absolute  : int = None    #: Absolute character position (file offset) since document start.

	def __init__(self, row : int, column : int, absolute : int):
		self.Row =       row
		self.Column =    column
		self.Absolute =  absolute

	def __str__(self):
		"""Returns a string representation."""
		return "(line: {0}, col: {1})".format(self.Row, self.Column)

	def __repr__(self):
		"""Returns a string representation in `row:col` format."""
		return "{0}:{1})".format(self.Row, self.Column)


class Token:
	def __init__(self, previousToken, start, end=None):
		previousToken.NextToken = self
		self._previousToken =     previousToken
		self.NextToken =          None
		self.Start =              start
		self.End =                end

	def __len__(self):
		return self.End.Absolute - self.Start.Absolute + 1

	@property
	def PreviousToken(self):
		return self._previousToken
	@PreviousToken.setter
	def PreviousToken(self, value):
		self._previousToken = value
		value.NextToken =     self

	# @property
	# def NextToken(self):
	# 	return self._nextToken
	# @NextToken.setter
	# def NextToken(self, value):
	# 	self._nextToken = value

	@property
	def Length(self):
		return len(self)

	def __str__(self):
		return repr(self) + " at " + str(self.Start)


class SuperToken(Token):
	def __init__(self, startToken, endToken=None):
		super().__init__(startToken.PreviousToken, startToken.Start, endToken.End if endToken else None)
		self.StartToken = startToken
		self.EndToken =   endToken

	def __iter__(self):
		token = self.StartToken
		while (token is not self.EndToken):
			yield token
			token = token.NextToken
		yield self.EndToken


class ValuedToken(Token):
	def __init__(self, previousToken, value, start, end=None):
		super().__init__(previousToken, start, end)
		self.Value =  value


class StartOfDocumentToken(ValuedToken):
	def __init__(self):
		self._previousToken =     None
		self._nextToken =         None
		self.Value =              None
		self.Start =              SourceCodePosition(1, 1, 1)
		self.End =                None

	def __len__(self):
		return 0

	def __str__(self):
		return "<StartOfDocumentToken>"


class CharacterToken(ValuedToken):
	def __init__(self, previousToken, value, start):
		if (len(value) != 1):    raise ValueError()
		super().__init__(previousToken, value, start=start, end=start)

	def __len__(self):
		return 1

	__CHARACTER_TRANSLATION__ = {
		"\r":    "CR",
		"\n":    "NL",
		"\t":    "TAB",
		" ":     "SPACE"
	}

	def __str__(self):
		return "<CharacterToken '{char}' at {line}:{col}>".format(
						char=self.__repr__(), pos=self.Start.Absolute, line=self.Start.Row, col=self.Start.Column)

	def __repr__(self):
		if (self.Value in self.__CHARACTER_TRANSLATION__):
			return self.__CHARACTER_TRANSLATION__[self.Value]
		else:
			return self.Value


class SpaceToken(ValuedToken):
	def __str__(self):
		return "<SpaceToken '{value}' at {line}:{col}>".format(
						value=self.Value, pos=self.Start.Absolute, line=self.Start.Row, col=self.Start.Column)


class DelimiterToken(ValuedToken):
	def __str__(self):
		return "<DelimiterToken '{value}' at {line}:{col}>".format(
						value=self.Value, pos=self.Start.Absolute, line=self.Start.Row, col=self.Start.Column)

class NumberToken(ValuedToken):
	def __str__(self):
		return "<NumberToken '{value}' at {line}:{col}>".format(
						value=self.Value, pos=self.Start.Absolute, line=self.Start.Row, col=self.Start.Column)

class StringToken(ValuedToken):
	def __str__(self):
		return "<StringToken '{value}' at {line}:{col}>".format(
						value=self.Value, pos=self.Start.Absolute, line=self.Start.Row, col=self.Start.Column)

class Tokenizer:
	class TokenKind(Enum):
		"""Enumeration of token kinds."""
		SpaceChars =      0
		AlphaChars =      1
		NumberChars =     2
		DelimiterChars =  3
		OtherChars =      4

	@staticmethod
	def GetCharacterTokenizer(iterable):
		previousToken =  None
		absolute =    0
		column =      0
		row =         1
		for char in iterable:
			absolute += 1
			column +=   1
			previousToken = CharacterToken(previousToken, char, SourceCodePosition(row, column, absolute))
			yield previousToken
			if (char == "\n"):
				column =  0
				row +=    1

	__ALPHA_CHARS__ =   "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"  #: Definition of word characters
	__NUMBER_CHARS__ =  "0123456789"                                            #: Definition of digit characters
	__SPACE_CHARS__ =   " \t"                                                   #: Definition of whitespace characters

	@classmethod
	def GetWordTokenizer(cls, iterable, alphaCharacters=__ALPHA_CHARS__, numberCharacters=__NUMBER_CHARS__, whiteSpaceCharacters=__SPACE_CHARS__):
		previousToken = StartOfDocumentToken()
		tokenKind =     cls.TokenKind.OtherChars
		start =         SourceCodePosition(1, 1, 1)
		buffer =        ""
		absolute =      0
		column =        0
		row =           1

		yield previousToken

		for char in iterable:
			absolute +=   1
			column +=     1

			if (tokenKind is cls.TokenKind.SpaceChars):
				if (char in whiteSpaceCharacters):
					buffer += char
				else:
					previousToken = SpaceToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken

					start =  SourceCodePosition(row, column, absolute)
					buffer = char
					if (char in alphaCharacters):
						tokenKind = cls.TokenKind.AlphaChars
					elif (char in numberCharacters):
						tokenKind = cls.TokenKind.NumberChars
					else:
						tokenKind = cls.TokenKind.OtherChars
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken
			elif (tokenKind is cls.TokenKind.AlphaChars):
				if (char in alphaCharacters):
					buffer += char
				else:
					previousToken = StringToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken

					start = SourceCodePosition(row, column, absolute)
					buffer = char
					if (char in " \t"):
						tokenKind = cls.TokenKind.SpaceChars
					elif (char in numberCharacters):
						tokenKind = cls.TokenKind.NumberChars
					else:
						tokenKind = cls.TokenKind.OtherChars
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken
			elif (tokenKind is cls.TokenKind.NumberChars):
				if (char in numberCharacters):
					buffer += char
				else:
					previousToken = NumberToken(previousToken, buffer, start,SourceCodePosition(row, column, absolute))
					yield previousToken

					start = SourceCodePosition(row, column, absolute)
					buffer = char
					if (char in " \t"):
						tokenKind = cls.TokenKind.SpaceChars
					elif (char in alphaCharacters):
						tokenKind = cls.TokenKind.AlphaChars
					else:
						tokenKind = cls.TokenKind.OtherChars
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken
			elif (tokenKind is cls.TokenKind.OtherChars):
				start = SourceCodePosition(row, column, absolute)
				buffer =      char
				if (char in " \t"):
					tokenKind =   cls.TokenKind.SpaceChars
				elif (char in alphaCharacters):
					tokenKind =   cls.TokenKind.AlphaChars
				elif (char in numberCharacters):
					tokenKind =   cls.TokenKind.NumberChars
				else:
					previousToken = CharacterToken(previousToken, char, start)
					yield previousToken
			else:
				raise ParserException("Unknown state.")

			if (char == "\n"):
				column =  0
				row +=    1
		# end for
