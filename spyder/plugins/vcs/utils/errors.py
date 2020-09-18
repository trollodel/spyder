#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2009- Spyder Project Contributors
#
# Distributed under the terms of the MIT License
# (see spyder/__init__.py for details)
# -----------------------------------------------------------------------------
"""A collection of VCS exceptions."""

# Standard library imports
import typing


class VCSError(Exception):
    """
    The base for all VCS errors.

    Parameters
    ----------
    error : str, optional
        The formatted error. Should respect the spec guidelines if any.
        The default is None.
    raw_error : str, optional
        The raw error message returned by the VCS. The default is None.
    """
    # HINT: No specification define the message format.

    __slots__ = ("error", "raw_error")

    def __init__(self,
                 error: typing.Optional[str] = None,
                 raw_error: typing.Optional[str] = None):
        args = []
        if error:
            args.append(error)
        if raw_error:
            args.append(raw_error)

        super().__init__(*args)
        self.error = error
        self.raw_error = raw_error


class VCSUnexpectedError(VCSError):
    """
    Raised when a bad error is occurred.

    Parameters
    ----------
    method : str, optional
        The method where the error occurred. The default is None.

    Notes
    -----
    This error is never raised by properties.

    See Also
    --------
    VCSPropertyError
    """

    __slots__ = ("method", )

    def __init__(self,
                 *args: object,
                 method: typing.Optional[str] = None,
                 **kwargs: typing.Optional[str]):
        super().__init__(*args, **kwargs)
        self.method = method


class VCSPropertyError(VCSError):
    """
    Raised when an operation on a property fails.

    Parameters
    ----------
    name : str
        The property name, this usually refers
        to the property name in the backend.
    operation : str
        The operation done to the property.
        Accepted values are: get, set, del.

    Notes
    -----
    This error is never raised by methods.

    See Also
    --------
    VCSUnexpectedError
    """

    __slots__ = ("name", "operation")

    def __init__(self, name: str, operation: str, *args: object,
                 **kwargs: typing.Optional[str]):
        super().__init__(*args, **kwargs)
        self.name = name
        operation = operation.lstrip("f")
        if operation in ("get", "set", "del"):
            self.operation = operation


class VCSBackendFail(VCSError):
    """
    Raised when a backend cannot initialize itself.

    This exception is raised for missing dependencies
    and missing repository in folder.

    Parameters
    ----------
    directory : str
        The directory given to the backend.
    backend_type : type
        The backend that raise the error
    programs : list, optional
        A list of missing executables. The default is an empty list.
    modules : list, optional
        A list of missing python modules. The default is an empty list.
    is_valid_repository : bool, optional
        A flag indicating if the directory contains a valid repository.
        The default is True.

        .. note::
            Module does refer to actual import-style module name,
            not pip package name.
    """
    __slots__ = ("directory", "backend_type", "programs", "modules",
                 "is_valid_repository")

    def __init__(self,
                 directory: str,
                 backend_type: type,
                 *args: object,
                 programs: typing.Iterable[str] = (),
                 modules: typing.Iterable[str] = (),
                 is_valid_repository: bool = True,
                 **kwargs: typing.Optional[str]):

        super().__init__(*args, **kwargs)
        self.directory = directory
        self.backend_type = backend_type
        self.programs = programs
        self.modules = modules
        self.is_valid_repository = is_valid_repository

    @property
    def missing_dependencies(self) -> bool:
        """Check if there are missing dependencies."""
        return any((self.programs, self.modules))


class VCSAuthError(VCSError):
    """
    Raised when an authentication error occurred.

    Parameters
    ----------
    username : str, optional
        The set username. The default is None.
    password : str, optional
        The set password. The default is None.
    email : str, optional
        The set email. The default is None.
    token : str, optional
        The set token. The default is None.
    required_credentials : str, optional
        The credentials that the backend requires.
    """

    __slots__ = ("username", "password", "email", "token",
                 "required_credentials")

    def __init__(self,
                 required_credentials: typing.Sequence[str],
                 *args: object,
                 username: typing.Optional[str] = None,
                 password: typing.Optional[str] = None,
                 email: typing.Optional[str] = None,
                 token: typing.Optional[str] = None,
                 **kwargs: typing.Optional[str]):

        super().__init__(*args, **kwargs)
        self.required_credentials = required_credentials
        self.username = username
        self.password = password
        self.email = email
        self.token = token

    @property
    def are_credentials_inserted(self) -> bool:
        """Check if the required credentials was inserted."""
        return all(
            getattr(self, key, None) is None
            for key in self.required_credentials)
