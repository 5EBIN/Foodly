import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  RefreshControl,
  Alert,
} from 'react-native';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { orderService } from '../services/api';
import { Order } from '../types';

export default function OrdersScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const queryClient = useQueryClient();

  const { data: orders = [], isLoading, error } = useQuery({
    queryKey: ['orders'],
    queryFn: orderService.getOrders,
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const acceptOrderMutation = useMutation({
    mutationFn: orderService.acceptOrder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      Alert.alert('Success', 'Job accepted successfully!');
    },
    onError: (error) => {
      Alert.alert('Error', 'Failed to accept job. Please try again.');
    },
  });

  const onRefresh = async () => {
    setRefreshing(true);
    await queryClient.invalidateQueries({ queryKey: ['orders'] });
    setRefreshing(false);
  };

  const handleAcceptOrder = (orderId: string) => {
    Alert.alert(
      'Accept Job',
      'Are you sure you want to accept this job?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Accept', onPress: () => acceptOrderMutation.mutate(orderId) },
      ]
    );
  };

  const renderOrderItem = ({ item }: { item: Order }) => (
    <View className="bg-white rounded-lg shadow-md p-4 mb-3 mx-4">
      <View className="flex-row justify-between items-start mb-2">
        <Text className="text-lg font-semibold text-gray-800">
          Order #{item.id}
        </Text>
        <View className="bg-green-100 px-2 py-1 rounded">
          <Text className="text-green-800 text-xs font-medium">
            {item.eta} min ETA
          </Text>
        </View>
      </View>

      <View className="mb-3">
        <Text className="text-gray-600 text-sm mb-1">
          <Text className="font-medium">Pickup:</Text> {item.pickup}
        </Text>
        <Text className="text-gray-600 text-sm">
          <Text className="font-medium">Dropoff:</Text> {item.dropoff}
        </Text>
      </View>

      <View className="flex-row justify-between items-center mb-3">
        <View className="flex-row space-x-4">
          <View className="bg-blue-100 px-2 py-1 rounded">
            <Text className="text-blue-800 text-xs">
              G-Value: {item.g_mean.toFixed(2)}
            </Text>
          </View>
          <View className="bg-orange-100 px-2 py-1 rounded">
            <Text className="text-orange-800 text-xs">
              Variance: {item.g_var.toFixed(2)}
            </Text>
          </View>
        </View>
      </View>

      <TouchableOpacity
        className="bg-blue-600 rounded-lg py-3"
        onPress={() => handleAcceptOrder(item.id)}
        disabled={acceptOrderMutation.isPending}
      >
        <Text className="text-white text-center font-semibold">
          {acceptOrderMutation.isPending ? 'Accepting...' : 'Accept Job'}
        </Text>
      </TouchableOpacity>
    </View>
  );

  if (isLoading && !refreshing) {
    return (
      <View className="flex-1 justify-center items-center bg-gray-50">
        <Text className="text-gray-600 text-lg">Loading available jobs...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View className="flex-1 justify-center items-center bg-gray-50 px-4">
        <Text className="text-red-600 text-lg text-center mb-4">
          Failed to load jobs
        </Text>
        <TouchableOpacity
          className="bg-blue-600 rounded-lg px-6 py-3"
          onPress={onRefresh}
        >
          <Text className="text-white font-semibold">Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-gray-50">
      <View className="bg-white px-4 py-3 border-b border-gray-200">
        <Text className="text-gray-600 text-sm">
          {orders.length} available jobs
        </Text>
      </View>

      <FlatList
        data={orders}
        renderItem={renderOrderItem}
        keyExtractor={(item) => item.id}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={{ paddingVertical: 8 }}
        ListEmptyComponent={
          <View className="flex-1 justify-center items-center py-20">
            <Text className="text-gray-500 text-lg text-center">
              No available jobs at the moment
            </Text>
            <Text className="text-gray-400 text-sm text-center mt-2">
              Pull down to refresh
            </Text>
          </View>
        }
      />
    </View>
  );
}
