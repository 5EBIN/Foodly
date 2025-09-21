import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { authService } from '../services/api';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigation = useNavigation();

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    setLoading(true);
    try {
      await authService.login({ email, password });
      navigation.navigate('Main' as never);
    } catch (error) {
      Alert.alert('Login Failed', 'Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = () => {
    Alert.alert(
      'Register',
      'Registration feature coming soon! For now, use any email/password to login.',
      [{ text: 'OK' }]
    );
  };

  return (
    <KeyboardAvoidingView 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      className="flex-1 bg-gray-50"
    >
      <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
        <View className="flex-1 justify-center px-8">
          <View className="bg-white rounded-lg shadow-lg p-8">
            <Text className="text-3xl font-bold text-center text-blue-600 mb-2">
              CN Project
            </Text>
            <Text className="text-lg text-center text-gray-600 mb-8">
              Worker Portal
            </Text>

            <View className="mb-4">
              <Text className="text-gray-700 mb-2">Email</Text>
              <TextInput
                className="border border-gray-300 rounded-lg px-4 py-3 text-gray-800"
                placeholder="Enter your email"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
                autoCorrect={false}
              />
            </View>

            <View className="mb-6">
              <Text className="text-gray-700 mb-2">Password</Text>
              <TextInput
                className="border border-gray-300 rounded-lg px-4 py-3 text-gray-800"
                placeholder="Enter your password"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
                autoCapitalize="none"
                autoCorrect={false}
              />
            </View>

            <TouchableOpacity
              className={`bg-blue-600 rounded-lg py-3 mb-4 ${
                loading ? 'opacity-50' : ''
              }`}
              onPress={handleLogin}
              disabled={loading}
            >
              <Text className="text-white text-center text-lg font-semibold">
                {loading ? 'Signing In...' : 'Sign In'}
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              className="bg-gray-200 rounded-lg py-3"
              onPress={handleRegister}
            >
              <Text className="text-gray-700 text-center text-lg font-semibold">
                Register
              </Text>
            </TouchableOpacity>

            <View className="mt-6 p-4 bg-blue-50 rounded-lg">
              <Text className="text-blue-800 text-sm text-center">
                Demo Mode: Use any email/password to login
              </Text>
            </View>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
