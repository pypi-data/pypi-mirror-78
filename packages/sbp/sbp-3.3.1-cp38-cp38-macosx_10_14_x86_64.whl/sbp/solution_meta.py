#!/usr/bin/env python
# Copyright (C) 2015-2018 Swift Navigation Inc.
# Contact: Swift Navigation <dev@swiftnav.com>
#
# This source is subject to the license found in the file 'LICENSE' which must
# be be distributed together with this source. All other rights reserved.
#
# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.


"""
Standardized Metadata messages for Fuzed Solution from Swift Navigation devices.
"""

import json

import construct

from sbp.msg import SBP, SENDER_ID
from sbp.utils import fmt_repr, exclude_fields, walk_json_dict, containerize

# Automatically generated from piksi/yaml/swiftnav/sbp/solution_meta.yaml with generate.py.
# Please do not hand edit!


class SolutionInputType(object):
  """SolutionInputType.
  
  Metadata describing which sensors were involved in the solution.
The structure is fixed no matter what the actual sensor type is.
The sensor_type field tells you which sensor we are talking about. It also tells you
whether the sensor data was actually used or not.
The flags field, always a u8, contains the sensor-specific data.
The content of flags, for each sensor type, is described in the relevant structures in this section.

  
  Parameters
  ----------
  sensor_type : int
    The type of sensor
  flags : int
    Refer to each InputType description

  """
  _parser = construct.Embedded(construct.Struct(
                     'sensor_type' / construct.Int8ul,
                     'flags' / construct.Int8ul,))
  __slots__ = [
               'sensor_type',
               'flags',
              ]

  def __init__(self, payload=None, **kwargs):
    if payload:
      self.from_binary(payload)
    else:
      self.sensor_type = kwargs.pop('sensor_type')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)
  
  def from_binary(self, d):
    p = SolutionInputType._parser.parse(d)
    for n in self.__class__.__slots__:
      setattr(self, n, getattr(p, n))

  def to_binary(self):
    d = dict([(k, getattr(obj, k)) for k in self.__slots__])
    return SolutionInputType.build(d)
    
SBP_MSG_SOLN_META = 0xFF0F
class MsgSolnMeta(SBP):
  """SBP class for message MSG_SOLN_META (0xFF0F).

  You can have MSG_SOLN_META inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message contains all metadata about the sensors received and/or used in computing the Fuzed Solution.
It focuses primarly, but not only, on GNSS metadata.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  pdop : int
    Position Dilution of Precision, as per last available DOPS from Starling GNSS engine
  hdop : int
    Horizontal Dilution of Precision, as per last available DOPS from Starling GNSS engine
  vdop : int
    Vertical Dilution of Precision, as per last available DOPS from Starling GNSS engine
  n_sats : int
    Number of satellites, as per last available solution from Starling GNSS engine
  age_corrections : int
    Age of the corrections (0xFFFF indicates invalid), as per last available AGE_CORRECTIONS from Starling GNSS engine
  alignment_status : int
    Bits for reason why it cannot align (yet)
  last_used_gnss_pos_tow : int
    Tow of last-used GNSS position measurement
  last_used_gnss_vel_tow : int
    Tow of last-used GNSS velocity measurement
  sol_in : array
    Array of Metadata describing the sensors potentially involved in the solution. Each element in the array represents a single sensor type and consists of flags containing (meta)data pertaining to that specific single sensor. Refer to each (XX)InputType descriptor in the present doc.
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'pdop' / construct.Int16ul,
                   'hdop' / construct.Int16ul,
                   'vdop' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'age_corrections' / construct.Int16ul,
                   'alignment_status' / construct.Int8ul,
                   'last_used_gnss_pos_tow' / construct.Int32ul,
                   'last_used_gnss_vel_tow' / construct.Int32ul,
                   construct.GreedyRange('sol_in' / construct.Struct(SolutionInputType._parser)),)
  __slots__ = [
               'pdop',
               'hdop',
               'vdop',
               'n_sats',
               'age_corrections',
               'alignment_status',
               'last_used_gnss_pos_tow',
               'last_used_gnss_vel_tow',
               'sol_in',
              ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgSolnMeta,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgSolnMeta, self).__init__()
      self.msg_type = SBP_MSG_SOLN_META
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.pdop = kwargs.pop('pdop')
      self.hdop = kwargs.pop('hdop')
      self.vdop = kwargs.pop('vdop')
      self.n_sats = kwargs.pop('n_sats')
      self.age_corrections = kwargs.pop('age_corrections')
      self.alignment_status = kwargs.pop('alignment_status')
      self.last_used_gnss_pos_tow = kwargs.pop('last_used_gnss_pos_tow')
      self.last_used_gnss_vel_tow = kwargs.pop('last_used_gnss_vel_tow')
      self.sol_in = kwargs.pop('sol_in')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgSolnMeta.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgSolnMeta(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    p = MsgSolnMeta._parser.parse(d)
    for n in self.__class__.__slots__:
      setattr(self, n, getattr(p, n))

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgSolnMeta._parser.build(c)
    return self.pack()

  def into_buffer(self, buf, offset):
    """Produce a framed/packed SBP message into the provided buffer and offset.

    """
    self.payload = containerize(exclude_fields(self))
    self.parser = MsgSolnMeta._parser
    self.stream_payload.reset(buf, offset)
    return self.pack_into(buf, offset, self._build_payload)

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgSolnMeta, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_GNSSInputType = 0xFFE7
class Gnssinputtype(SBP):
  """SBP class for message GNSSInputType (0xFFE7).

  You can have GNSSInputType inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  Metadata around the GNSS sensors involved in the fuzed solution. Accessible through sol_in[N].flags
                                                                        in a MSG_SOLN_META.
Note: Just to build descriptive tables in documentation and not actually used.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  flags : int
    flags that store all relevant info specific to this sensor type.
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'flags',
              ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( Gnssinputtype,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( Gnssinputtype, self).__init__()
      self.msg_type = SBP_GNSSInputType
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return Gnssinputtype.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return Gnssinputtype(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    p = Gnssinputtype._parser.parse(d)
    for n in self.__class__.__slots__:
      setattr(self, n, getattr(p, n))

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = Gnssinputtype._parser.build(c)
    return self.pack()

  def into_buffer(self, buf, offset):
    """Produce a framed/packed SBP message into the provided buffer and offset.

    """
    self.payload = containerize(exclude_fields(self))
    self.parser = Gnssinputtype._parser
    self.stream_payload.reset(buf, offset)
    return self.pack_into(buf, offset, self._build_payload)

  def to_json_dict(self):
    self.to_binary()
    d = super( Gnssinputtype, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_IMUInputType = 0xFFE8
class Imuinputtype(SBP):
  """SBP class for message IMUInputType (0xFFE8).

  You can have IMUInputType inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  Metadata around the IMU sensors involved in the fuzed solution. Accessible through sol_in[N].flags
                                                                       in a MSG_SOLN_META.
Note: Just to build descriptive tables in documentation and not actually used.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  flags : int
    flags that store all relevant info specific to this sensor type.
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'flags',
              ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( Imuinputtype,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( Imuinputtype, self).__init__()
      self.msg_type = SBP_IMUInputType
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return Imuinputtype.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return Imuinputtype(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    p = Imuinputtype._parser.parse(d)
    for n in self.__class__.__slots__:
      setattr(self, n, getattr(p, n))

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = Imuinputtype._parser.build(c)
    return self.pack()

  def into_buffer(self, buf, offset):
    """Produce a framed/packed SBP message into the provided buffer and offset.

    """
    self.payload = containerize(exclude_fields(self))
    self.parser = Imuinputtype._parser
    self.stream_payload.reset(buf, offset)
    return self.pack_into(buf, offset, self._build_payload)

  def to_json_dict(self):
    self.to_binary()
    d = super( Imuinputtype, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_OdoInputType = 0xFFE9
class Odoinputtype(SBP):
  """SBP class for message OdoInputType (0xFFE9).

  You can have OdoInputType inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  Metadata around the Odometry sensors involved in the fuzed solution. Accessible through sol_in[N].flags
                                                                            in a MSG_SOLN_META.
Note: Just to build descriptive tables in documentation and not actually used.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  flags : int
    flags that store all relevant info specific to this sensor type.
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'flags',
              ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( Odoinputtype,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( Odoinputtype, self).__init__()
      self.msg_type = SBP_OdoInputType
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return Odoinputtype.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return Odoinputtype(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    p = Odoinputtype._parser.parse(d)
    for n in self.__class__.__slots__:
      setattr(self, n, getattr(p, n))

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = Odoinputtype._parser.build(c)
    return self.pack()

  def into_buffer(self, buf, offset):
    """Produce a framed/packed SBP message into the provided buffer and offset.

    """
    self.payload = containerize(exclude_fields(self))
    self.parser = Odoinputtype._parser
    self.stream_payload.reset(buf, offset)
    return self.pack_into(buf, offset, self._build_payload)

  def to_json_dict(self):
    self.to_binary()
    d = super( Odoinputtype, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    

msg_classes = {
  0xFF0F: MsgSolnMeta,
  0xFFE7: Gnssinputtype,
  0xFFE8: Imuinputtype,
  0xFFE9: Odoinputtype,
}