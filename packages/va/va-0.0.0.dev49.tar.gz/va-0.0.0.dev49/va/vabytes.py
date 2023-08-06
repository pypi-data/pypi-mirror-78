import sys
# if sys.version_info < (3,):
#     def tobytes(x):
#         print('2version')
#         return x
# else:
#     import codecs
#     def tobytes(x):
#         print('3version')
#         return codecs.latin_1_encode(x)[0]



# if sys.version_info[0] > 2:
#     def __bytes__(self):
#         return self.__str__().encode('utf-8')
#
#     def __str__(self):
#         string = self._unicode()
#         return str(string)
# else:
#     def __str__(self):
#         return self.__unicode__().encode('utf-8')
#
#     def __unicode__(self):
#         string = self._unicode()
#         return _str(string)


if sys.version_info[0] >= 3: # Python 3
  def __str__(self):
      return self.__unicode__()
else:  # Python 2
  def __str__(self):
      return self.__unicode__().encode('utf8')